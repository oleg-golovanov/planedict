# -*- coding: utf-8 -*-


import unittest

from planedict import PlaneDict


class PlaneTest(unittest.TestCase):

    def setUp(self):
        self.flat = PlaneDict(
            {'key1': {'key2': 'val2', 'key3': 'val3'}, 'key4': {'key5': {'key6': 'val6'}}}
        )

    def test_check_path(self):
        self.assertEqual(
            self.flat.__check_path__((1, [2, [3]], 4, (5, 6), (i for i in [7, 8]))),
            (1, 2, 3, 4, (5, 6), 7, 8)
        )

    # overridden methods
    def test_init(self):
        self.assertEqual(
            PlaneDict(zip([1, 3], [2, 4])),
            PlaneDict({1: 2, 3: 4})
        )

    def test_iter(self):
        self.assertEqual(
            list(self.flat),
            [('key1', 'key3'), ('key1', 'key2'), ('key4', 'key5', 'key6')]
        )

    def test_len(self):
        self.assertEqual(
            len(self.flat),
            3
        )

    def test_repr(self):
        self.assertEqual(
            repr(self.flat),
            repr(self.flat.__dict__)
        )

    def test_getitem(self):
        path = ['key4', 'key5', 'key6']

        self.assertEqual(
            self.flat[path],
            'val6'
        )

        self.assertRaises(
            KeyError,
            self.flat.__getitem__,
            (path, [2])
        )

    def test_setitem(self):
        path = 'key1', 'key2', 'key10'
        value = 1

        self.flat[path] = value
        self.assertEqual(
            self.flat[path],
            value
        )

    def test_delitem(self):
        del self.flat['key4', 'key5', 'key6']
        self.assertEqual(
            self.flat,
            PlaneDict({'key1': {'key3': 'val3', 'key2': 'val2'}})
        )

        path = ['key1', 'key2']

        self.assertRaises(
            KeyError,
            self.flat.__delitem__,
            (path, [1])
        )

        self.assertRaises(
            KeyError,
            self.flat.__delitem__,
            (path, [1, 2])
        )

    def test_get(self):
        expected = {'key2': 'val2', 'key3': 'val3'}

        self.assertEqual(
            self.flat.get('key1'),
            PlaneDict(expected)
        )

        self.assertEqual(
            self.flat.get('key1', stddict=True),
            expected
        )

    # inherited methods
    def test_clear(self):
        self.assertFalse(
            self.flat.clear()
        )

    def test_pop(self):
        path = ['key4', 'key5', 'key6']

        self.assertEqual(
            self.flat.pop(path, default=None),
            'val6'
        )

        path.pop()
        self.assertEqual(
            self.flat.pop(path, default=None),
            None
        )

        path.pop()
        self.assertEqual(
            self.flat.pop(path, default=None),
            None
        )

    def test_popitem(self):
        self.assertEqual(
            self.flat.popitem(),
            (('key1', 'key3'), 'val3')
        )

        self.assertEqual(
            self.flat.popitem(),
            (('key1', 'key2'), 'val2')
        )

        self.assertEqual(
            self.flat.popitem(),
            (('key4', 'key5', 'key6'), 'val6')
        )

        self.assertRaises(
            KeyError,
            self.flat.popitem
        )

    def test_setdefault(self):
        self.assertEqual(
            self.flat.setdefault(['key1', 'key2'], default=None),
            'val2'
        )

        self.assertEqual(
            self.flat.setdefault(['key1', 'key7', 'key8', 'key9'], default=None),
            None
        )

        self.assertEqual(
            self.flat.get('key1', stddict=True),
            {'key2': 'val2', 'key3': 'val3', 'key7': {'key8': {'key9': None}}}
        )

    def test_update(self):
        update = {'key1': {'key10': 'val10'}}

        self.flat.update(PlaneDict(update))
        self.assertEqual(
            self.flat.__dict__,
            {'key1': {'key2': 'val2', 'key3': 'val3', 'key10': 'val10'}, 'key4': {'key5': {'key6': 'val6'}}}
        )

        self.flat.update(update)
        self.assertEqual(
            self.flat.__dict__,
            {'key1': {'key10': 'val10'}, 'key4': {'key5': {'key6': 'val6'}}}
        )

    def test_keys(self):
        self.assertEqual(
            self.flat.keys(),
            [('key1', 'key3'), ('key1', 'key2'), ('key4', 'key5', 'key6')]
        )

    def test_values(self):
        self.assertEqual(
            self.flat.values(),
            ['val3', 'val2', 'val6']
        )

    def test_items(self):
        self.assertEqual(
            self.flat.items(),
            [(('key1', 'key3'), 'val3'), (('key1', 'key2'), 'val2'), (('key4', 'key5', 'key6'), 'val6')]
        )

    def test_contains(self):
        self.assertTrue(
            ['key1', 'key2'] in self.flat
        )

        self.assertFalse(
            ['key1', 'missed_key'] in self.flat
        )

    def test_eq(self):
        eq = {'key1': {'key2': 'val2', 'key3': 'val3'}, 'key4': {'key5': {'key6': 'val6'}}}
        self.assertEqual(
            self.flat,
            PlaneDict(eq)
        )

    def test_ne(self):
        ne = {'key1': {'key2': 'val2', 'key3': 'val3'}}
        self.assertNotEqual(
            self.flat,
            PlaneDict(ne)
        )


if __name__ == '__main__':
    unittest.main()
