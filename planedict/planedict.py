# -*- coding: utf-8 -*-


"""
PlaneDict is a dict-like class which represents built-in dict class
as a 'plane' structure, i.e. path-value pairs. Path is a tuple of keys,
value is a value which allows in built-in dict.

Supported methods:
    * native:
        * __check_path__(self, path)
    * overridden:
        * __init__(self, seq=None, _factory=dict, **kwargs)
        * __getitem__(self, path)
        * __setitem__(self, path, value)
        * __delitem__(self, path)
        * __iter__(self)
        * __len__(self)
        * __repr__(self)
        * get(self, key, default=None, stddict=False)
    * inherited:
        * clear(self)
        * pop(self, key, default=<object object>)
        * popitem(self)
        * setdefault(self, key, default=None)
        * update(*args, **kwds)
        * __contains__(self, key)
        * __eq__(self, other)
        * __ne__(self, other)
        * keys(self)
        * iterkeys(self)
        * values(self)
        * itervalues(self)
        * items(self)
        * iteritems(self)

NOTES:
    1. Constructor have _factory argument, it expects dict-like class (dict by default).
       OrderedDict is useful to use.
    2. After removing value by path, if higher dicts will become
       empty, they will be removed.
    3. get method has stddict parameter. If it's True then method will return
       built-in dict, it will return PlaneDict object or object inherited from it else.
    4. If PlaneDict object was passed to update method, it's a 'soft'
       update, i.e. the intersecting values will be overridden and the new
       values will be added.
       If standard dict passed to update method, it works as a
       standard update method.
    5. __check_path__ method takes a sequence of keys.
       For example: __check_path__((1, [2, [3]], 4, (5, 6), (i for i in [7, 8])))
       returns (1, 2, 3, 4, (5, 6), 7, 8). As you can see from the
       example above, tuple is not unfold, because tuple can be
       a key of dict. So if you want to get a single-key tuple,
       you should do this:
            d[('key',),]
            or
            path = 'key',
            d[path,]

       See examples.


EXAMPLES:
    > d = PlaneDict(
        {
            'key1': {
                'key2': 'val2',
                'key3': 'val3'
            },
            'key4': {
                'key5': {
                    'key6': 'val6'
                }
            }
        }
    )

    > len(d)
    3

    > d['key4', 'key5', 'key6']
    'val6'

    > path = ['key1', 'key2', 'key10']
    > d[path] = 1
    > d[path]
    1

    > del d['key4', 'key5', 'key6']
    > d
    {'key1': {'key3': 'val3', 'key2': 'val2'}}

    > list(d)
    [('key1', 'key3'),
     ('key1', 'key2'),
     ('key4', 'key5', 'key6')]

    > d.get('key1', stddict=True)
    {'key3': 'val3', 'key2': 'val2'}
    > d.get(('key1', 'key2'))
    'val2'

    > d.clear()
    > print d
    {}

    > d.pop(['key4', 'key5', 'key6'], default=None)
    'val6'
    > d.pop(['key4', 'key5', 'key6'], default=None)
    None

    > d.popitem()
    (('key1', 'key3'), 'val3')

    > d.setdefault(['key1', 'key2'], default=None)
    'val2'
    > d.setdefault(['key1', 'key7', 'key8', 'key9'], default=None)
    > d['key1']
    {'key3': 'val3', 'key2': 'val2', 'key7': {'key8': {'key9': None}}}

    > update = {'key1': {'key10': 'val10'}}
    > d.update(PlaneDict(update))
    > d
    {'key1': {'key2': 'val2', 'key3': 'val3', 'key10': 'val10'}, 'key4': {'key5': {'key6': 'val6'}}}
    > d.update(update)
    > d
    {'key1': {'key10': 'val10'}, 'key4': {'key5': {'key6': 'val6'}}}

    > d.keys()
    [('key1', 'key3'),
     ('key1', 'key2'),
     ('key4', 'key5', 'key6')]

    > d.values()
    ['val3', 'val2', 'val6']

    > d.items()
    [(('key1', 'key3'), 'val3'),
     (('key1', 'key2'), 'val2'),
     (('key4', 'key5', 'key6'), 'val6')]

    > ['key1', 'key2'] in d
    True
    > ['key1', 'missed_key'] in d
    False

    > d == PlaneDict({'key1': {'key2': 'val2', 'key3': 'val3'}, 'key4': {'key5': {'key6': 'val6'}}})
    True

    > d == {'key1': {'key2': 'val2', 'key3': 'val3'}, 'key4': {'key5': {'key6': 'val6'}}}
    False
"""


import sys
import collections


NoneType = type(None)


PY3 = sys.version_info[0] == 3
PY33 = sys.version_info[0:2] >= (3, 3)
if PY3:
    def iteritems(d):
        return iter(d.items())
    basestring = str
else:
    from operator import methodcaller
    iteritems = methodcaller('iteritems')


class PlaneDict(collections.MutableMapping):

    __slots__ = (
        '_factory',
        '_dict',
        '_type'
    )
    if PY33:
        __slots__ += ('__weakref__',)

    def __init__(self, seq=None, _factory=dict, **kwargs):
        """
        Class constructor, takes the same arguments
        as the built-in dict class.
        _factory argument expects dict-like class (dict by default).
        OrderedDict is useful to use.
        """

        self._factory = _factory
        self._dict = _factory()
        self._type = type(self)

        self._dict.update(seq or [], **kwargs)

    def __getitem__(self, path):
        """
        Get value by path.
        """

        items = self._dict

        for key in self.__check_path__(path):
            if not isinstance(items, (dict, self._type)):
                raise KeyError(key)
            items = items[key]

        if isinstance(items, dict):
            items = self._type(items)

        return items

    def __setitem__(self, path, value):
        """
        Set value by path.
        """

        path = self.__check_path__(path)

        # d - dict, p - path (keys sequence)
        def set_key(d, p):
            k = p[0]

            if len(p) == 1:
                d[k] = value
            else:
                if not isinstance(d.setdefault(k, self._factory()), dict):
                    d[k] = self._factory()
                set_key(d[k], p[1:])

        set_key(self._dict, path)

    def __delitem__(self, path):
        """
        Remove value by path.
        If higher dicts will become empty, they will be removed.
        """

        path = self.__check_path__(path)

        # d - dict
        def is_empty(d):
            if not d:
                return True
            return False

        # d - dict, p - path (keys sequence)
        def remove_key(d, p):
            k = p[0]

            if len(p) == 1:
                if not isinstance(d, dict):
                    raise KeyError(k)
                del d[k]
                return is_empty(d)

            if not isinstance(d, dict):
                raise KeyError(k)
            if remove_key(d[k], p[1:]):
                del d[k]
                return is_empty(d)

        remove_key(self._dict, path)

    def __iter__(self):
        """
        Iterator over the keys of dict.
        """

        result = []

        # d - dict, p - path (keys sequence)
        def recurs_iter(d, p=None):
            p = p or []

            # k - key, v - value
            for k, v in iteritems(d):
                next_p = p + [k]
                if isinstance(v, dict):
                    recurs_iter(v, next_p)
                else:
                    result.append(tuple(next_p))

        recurs_iter(self._dict)

        return iter(result)

    def __len__(self):
        """
        Object length calculation.
        """

        return len(list(self.__iter__()))

    def __repr__(self):
        """
        Representation of the object is the same as
        representation of built-in dict class.
        """

        return repr(self._dict)

    def get(self, key, default=None, stddict=False):
        """
        Same as a dict class method.
        If stddict parameter is True then method will return built-in dict,
        it will return PlaneDict object or object inherited from it else.
        """

        result = super(self._type, self).get(key, default)
        if isinstance(result, self._type) and stddict:
            result = result._dict

        return result

    @staticmethod
    def __check_path__(path):
        """
        If path is a instance of basestring, int,
        float or complex classes, it will return single-key
        tuple with this instance.
        If path is a sequence of key, it will be unfold, as
        described in NOTES paragraph number 4 of __doc__.
        """

        def seq_iter(iterable):
            result = []
            for p in iterable:
                if isinstance(p, collections.Iterable) and \
                        not isinstance(p, (basestring, tuple)):
                    result += seq_iter(p)
                else:
                    result.append(p)

            return result

        if isinstance(path, (basestring, int, float, complex, NoneType)):
            return path,
        else:
            return tuple(seq_iter(path))
