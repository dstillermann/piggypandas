import unittest
from piggypandas import Mapper
import pandas as pd


class TestMapperBase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        df: pd.DataFrame = pd.DataFrame(data={
            'Name': ['Boris', 'Basil', 'Vincent', 'Murray'],
            'Species': ['Pig', 'Horse', 'Lamb', 'Mouse'],
            'Color': ['White', 'Black', 'Yellow', 'Gray']
        })
        xlsx_file_cs: str = '../tmp/demomapping-cs.xlsx'
        xlsx_file_ci: str = '../tmp/demomapping-ci.xlsx'
        df.to_excel(xlsx_file_cs, sheet_name='DATA', index=False)
        df.to_excel(xlsx_file_ci, sheet_name='DATA', index=False)
        self._mapper_cs: Mapper = Mapper(xlsx_file_cs, columns=['Name'], ignore_case=False)  # case-sensitive
        self._mapper_ci: Mapper = Mapper(xlsx_file_ci, columns=['Name'], ignore_case=True)  # case-insensitive

    def tearDown(self) -> None:
        self._mapper_cs.flush()
        self._mapper_ci.flush()
        super().tearDown()


class TestMapperReadOnlyOperations(TestMapperBase):

    def test_has(self):
        for m in [self._mapper_cs, self._mapper_ci]:
            self.assertTrue(m.has('Vincent'))
            self.assertFalse(m.has('InvalidKey'))
            self.assertTrue(m.hasc('Vincent', 'Color'))
            self.assertFalse(m.hasc('InvalidKey', 'Color'))
            self.assertFalse(m.hasc('Vincent', 'InvalidCol'))
            self.assertTrue(m.hasc('Vincent'))

    def test_get_no_defaultvalue(self):
        for m in [self._mapper_cs, self._mapper_ci]:
            self.assertEqual(m.get('Vincent'), 'Lamb')
            self.assertEqual(m.getc('Murray', 'Color'), 'Gray')
            self.assertEqual(m['Color'].get('Boris'), 'White')
            with self.assertRaises(KeyError):
                m.get('InvalidKey')
            with self.assertRaises(KeyError):
                m.getc('Boris', 'InvalidCol')
            with self.assertRaises(KeyError):
                m.getc('InvalidKey', 'InvalidCol')

    def test_has_caseinsensitive(self):
        for key in ['Vincent', 'VINCENT', 'ViNcEnT']:
            self.assertTrue(self._mapper_ci.has(key))
            for col in ['Color', 'color', 'ColOr']:
                self.assertTrue(self._mapper_ci.hasc(key, col))
                self.assertTrue(self._mapper_ci[col].has(key))

    def test_get_caseinsensitive(self):
        for key in ['Vincent', 'VINCENT', 'ViNcEnT']:
            for col in ['Color', 'color', 'ColOr']:
                self.assertEqual(self._mapper_ci.getc(key, col), 'Yellow')
                self.assertEqual(self._mapper_ci[col].get(key), 'Yellow')

    # noinspection PyStatementEffect
    def test_indexer(self):
        self.assertIsNotNone(self._mapper_cs['Species'])
        self.assertIsNotNone(self._mapper_ci['Species'])
        with self.assertRaises(KeyError):
            self._mapper_cs['InvalidCol']
        with self.assertRaises(KeyError):
            self._mapper_ci['InvalidCol']
        with self.assertRaises(KeyError):
            self._mapper_cs['SPECIES']
        self.assertIsNotNone(self._mapper_ci['SPECIES'])

    def test_touch_no_defaultvalue(self):
        for m in [self._mapper_cs, self._mapper_ci]:
            self.assertTrue(m.touch('Vincent'))
            self.assertTrue(m['Species'].touch('Vincent'))
            self.assertFalse(m.touchc('Vincent', 'Sex'))
            self.assertFalse(m.touch('Mary'))
            self.assertFalse(m['Species'].touch('Mary'))
            self.assertFalse(m.touchc('Mary', 'Sex'))


class TestMapperModifyingTouch(TestMapperBase):

    def test_touchc_defaultvalue(self):
        self.assertEqual(self._mapper_cs.size, 4)
        self.assertEqual(self._mapper_ci.size, 4)
        self.assertEqual(len(self._mapper_cs.columns), 3)
        self.assertEqual(len(self._mapper_ci.columns), 3)
        for m in [self._mapper_cs, self._mapper_ci]:
            self.assertTrue(m.touchc('Vincent', 'Species', 'Mutton'))
            self.assertEqual(m.getc('Vincent', 'Species'), 'Lamb')
            self.assertFalse(m.is_changed)
            self.assertTrue(m.touchc('Vincent', 'Sex', 'Male'))
            self.assertEqual(m.getc('Vincent', 'Sex'), 'Male')
            self.assertTrue(m.is_changed)
            self.assertTrue(m.touchc('Mary', 'Species', 'Rat'))
            self.assertEqual(m.getc('Mary', 'Species'), 'Rat')
            self.assertTrue(m.touchc('Mary', 'Sex', 'Female'))
            self.assertEqual(m.getc('Mary', 'Sex'), 'Female')
        self.assertEqual(self._mapper_cs.size, 5)
        self.assertEqual(self._mapper_ci.size, 5)
        self.assertEqual(len(self._mapper_cs.columns), 4)
        self.assertEqual(len(self._mapper_ci.columns), 4)


class TestMapperSet(TestMapperBase):

    def test_set(self):
        self.assertEqual(self._mapper_cs.size, 4)
        self.assertEqual(self._mapper_ci.size, 4)
        self.assertEqual(len(self._mapper_cs.columns), 3)
        self.assertEqual(len(self._mapper_ci.columns), 3)
        for m in [self._mapper_cs, self._mapper_ci]:
            for key, col, value in [
                ('Vincent', 'Species', 'Mutton'),
                ('VinCent', 'Species', 'Mutton'),
                ('Mary', 'Species', 'Hamster'),
                ('MarY', 'SPECIES', 'Hamster')
            ]:
                self.assertTrue(m.setc(key, col, value))
        self.assertEqual(self._mapper_cs.size, 7)
        self.assertEqual(self._mapper_ci.size, 5)
        self.assertEqual(len(self._mapper_cs.columns), 4)
        self.assertEqual(len(self._mapper_ci.columns), 3)


if __name__ == '__main__':
    unittest.main()
