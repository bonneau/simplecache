import unittest

from simplecache import SimpleCache
from unittest import TestCase


class BasicTests(TestCase):
    def test_basic_functionality(self):
        sc = SimpleCache(max_items=3)
        sc[1] = 'a'
        sc[2] = 'b'
        sc[3] = 'c'

        self.assertEqual(sc[1], 'a')
        self.assertEqual(sc[2], 'b')
        self.assertEqual(sc[3], 'c')
        self.assertEqual(len(sc), 3)

        sc[4] = 'd'
        self.assertEqual(sc[4], 'd')
        self.assertEqual(len(sc), 3)
        self.assertFalse(1 in sc)


if __name__ == '__main__':
    unittest.main()