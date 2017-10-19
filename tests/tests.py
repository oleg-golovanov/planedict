# -*- coding: utf-8 -*-


import unittest
from collections import OrderedDict

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
            set(self.flat),
            {('key1', 'key2'), ('key1', 'key3'), ('key4', 'key5', 'key6')}
        )

    def test_len(self):
        self.assertEqual(
            len(self.flat),
            3
        )

    def test_repr(self):
        self.assertEqual(
            repr(self.flat),
            repr(self.flat._dict)
        )

    def test_getitem(self):
        path = ['key4', 'key5', 'key6']
        flat = PlaneDict({'key1': PlaneDict({'key2': 'val2'})})

        self.assertEqual(
            self.flat[path],
            'val6'
        )

        self.assertRaises(
            KeyError,
            self.flat.__getitem__,
            (path, [2])
        )

        self.assertRaises(
            KeyError,
            self.flat.__getitem__,
            None
        )

        self.assertEqual(
            flat['key1', 'key2'],
            'val2'
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
            self.flat._dict,
            {'key1': {'key2': 'val2', 'key3': 'val3', 'key10': 'val10'}, 'key4': {'key5': {'key6': 'val6'}}}
        )

        self.flat.update(update)
        self.assertEqual(
            self.flat._dict,
            {'key1': {'key10': 'val10'}, 'key4': {'key5': {'key6': 'val6'}}}
        )

    def test_keys(self):
        self.assertEqual(
            set(self.flat.keys()),
            {('key1', 'key2'), ('key1', 'key3'), ('key4', 'key5', 'key6')}
        )

    def test_values(self):
        self.assertEqual(
            set(self.flat.values()),
            {'val2', 'val3', 'val6'}
        )

    def test_items(self):
        self.assertEqual(
            set(self.flat.items()),
            {(('key1', 'key2'), 'val2'), (('key1', 'key3'), 'val3'), (('key4', 'key5', 'key6'), 'val6')}
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


class PlaneOrderTest(unittest.TestCase):
    def setUp(self):
        self.items = (
            (('key1', 'key2'), 'val2'),
            (('key1', 'key3'), 'val3'),
            (('key4', 'key5', 'key6'), 'val6')
        )
        self.ordered_flat = PlaneDict(_factory=OrderedDict)
        for k, v in self.items:
            self.ordered_flat[k] = v

    def test_order(self):
        order = OrderedDict([
            ['key1', OrderedDict([
                ['key2', 'val2'],
                ['key3', 'val3']
            ])],
            ['key4', OrderedDict([
                ['key5', OrderedDict([
                    ['key6', 'val6']
                ])]
            ])]
        ])
        self.assertEqual(
            self.ordered_flat._dict,
            order
        )

    # inherited method
    def test_popitem(self):
        self.assertEqual(
            self.ordered_flat.popitem(),
            self.items[0]
        )

        self.assertEqual(
            self.ordered_flat.popitem(),
            self.items[1]
        )

        self.assertEqual(
            self.ordered_flat.popitem(),
            self.items[2]
        )

        self.assertRaises(
            KeyError,
            self.ordered_flat.popitem
        )


if __name__ == '__main__':
    unittest.main()
