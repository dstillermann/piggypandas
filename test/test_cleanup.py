import unittest
from piggypandas import Cleanup


class TestCleanup(unittest.TestCase):

    def test_cleanup(self):
        for (x, mode, y) in [
            ('  x  ', Cleanup.CASE_INSENSITIVE, 'X'),
            ('  x  ', Cleanup.CASE_SENSITIVE, 'x'),
            ('  x  ', Cleanup.NONE, '  x  ')
        ]:
            self.assertEqual(Cleanup.cleanup(x, mode), y)

    def test_eq(self):
        for (s1, s2, mode) in [
            ('xy', '    XY ', Cleanup.CASE_INSENSITIVE),
            ('x y', '    X Y ', Cleanup.CASE_INSENSITIVE),
            ('x', 'X', Cleanup.CASE_INSENSITIVE),
            ('x', 'x', Cleanup.NONE)
        ]:
            self.assertTrue(Cleanup.eq(s1, s2, mode))
        for (s1, s2, mode) in [
            ('xy', '    X    Y ', Cleanup.CASE_INSENSITIVE),
            ('x', 'X', Cleanup.CASE_SENSITIVE),
            ('x', 'X', Cleanup.NONE)
        ]:
            self.assertFalse(Cleanup.eq(s1, s2, mode))


if __name__ == '__main__':
    unittest.main()
