import unittest
from piggypandas import Cleanup


class TestCleanup(unittest.TestCase):

    def test_cleanup(self):
        for (x, mode, y) in [
            ('  X  ', Cleanup.CASE_INSENSITIVE, 'x'),
            ('  X  ', Cleanup.CASE_SENSITIVE, 'X'),
            ('  x  ', Cleanup.NONE, '  x  ')
        ]:
            self.assertEqual(Cleanup.cleanup(x, mode), y)

    def test_eq(self):
        for (s1, s2, mode) in [
            ('xy', '    xy ', Cleanup.CASE_INSENSITIVE),
            ('X Y', '    x y ', Cleanup.CASE_INSENSITIVE),
            ('X', 'x', Cleanup.CASE_INSENSITIVE),
            ('X', 'X', Cleanup.NONE)
        ]:
            self.assertTrue(Cleanup.eq(s1, s2, mode))
        for (s1, s2, mode) in [
            ('xy', '    x    y ', Cleanup.CASE_INSENSITIVE),
            ('X', 'x', Cleanup.CASE_SENSITIVE),
            ('x', 'X', Cleanup.NONE)
        ]:
            self.assertFalse(Cleanup.eq(s1, s2, mode))


if __name__ == '__main__':
    unittest.main()
