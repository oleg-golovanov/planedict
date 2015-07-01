PlaneDict
---------

PlaneDict is a dict-like class which represents built-in dict class
as a 'plane' structure, i.e. path-value pairs. Path is a tuple of keys,
value is a value which allows in built-in dict.

Supported methods:
    * native:
        * __check_path__(self, path)
    * overridden:
        * __init__(self, seq=None, _factory=dict, \**kwargs)
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
        * update(\*args, \**kwds)
        * __contains__(self, key)
        * __eq__(self, other)
        * __ne__(self, other)
        * keys(self)
        * iterkeys(self)
        * values(self)
        * itervalues(self)
        * items(self)
        * iteritems(self)

Installation
------------
::

    $ pip install planedict

Notes
-----
1. Constructor have _factory argument, it expects dict-like class (dict by default).
   OrderedDict is useful to use.
2. After removing value by path, if higher dicts will become
   empty, they will be removed.
3. get method has stddict parameter. If it's True then method will return
   built-in dict, it will return PlaneDict object else.
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

    .. code-block:: python

        d[('key',),]

    or

    .. code-block:: python

        path = 'key',
        d[path,]

See examples.


Examples
--------

.. code-block:: python

    d = PlaneDict(
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

    >>> len(d)
    3

    >>> d['key4', 'key5', 'key6']
    'val6'

    >>> path = ['key1', 'key2', 'key10']
    >>> d[path] = 1
    >>> d[path]
    1

    >>> del d['key4', 'key5', 'key6']
    >>> d
    {'key1': {'key3': 'val3', 'key2': 'val2'}}

    >>> list(d)
    [('key1', 'key3'),
     ('key1', 'key2'),
     ('key4', 'key5', 'key6')]

    >>> d.get('key1', stddict=True)
    {'key3': 'val3', 'key2': 'val2'}
    >>> d.get(('key1', 'key2'))
    'val2'

    >>> d.clear()
    >>> print d
    {}

    >>> d.pop(['key4', 'key5', 'key6'], default=None)
    'val6'
    >>> d.pop(['key4', 'key5', 'key6'], default=None)
    None

    >>> d.popitem()
    (('key1', 'key3'), 'val3')

    >>> d.setdefault(['key1', 'key2'], default=None)
    'val2'
    >>> d.setdefault(['key1', 'key7', 'key8', 'key9'], default=None)
    >>> d['key1']
    {'key3': 'val3', 'key2': 'val2', 'key7': {'key8': {'key9': None}}}

    >>> update = {'key1': {'key10': 'val10'}}
    >>> d.update(PlaneDict(update))
    >>> d
    {'key1': {'key2': 'val2', 'key3': 'val3', 'key10': 'val10'}, 'key4': {'key5': {'key6': 'val6'}}}
    >>> d.update(update)
    >>> d
    {'key1': {'key10': 'val10'}, 'key4': {'key5': {'key6': 'val6'}}}

    >>> d.keys()
    [('key1', 'key3'),
     ('key1', 'key2'),
     ('key4', 'key5', 'key6')]

    >>> d.values()
    ['val3', 'val2', 'val6']

    >>> d.items()
    [(('key1', 'key3'), 'val3'),
     (('key1', 'key2'), 'val2'),
     (('key4', 'key5', 'key6'), 'val6')]

    >>> ['key1', 'key2'] in d
    True
    >>> ['key1', 'missed_key'] in d
    False

    >>> d == PlaneDict({'key1': {'key2': 'val2', 'key3': 'val3'}, 'key4': {'key5': {'key6': 'val6'}}})
    True

    >>> d == {'key1': {'key2': 'val2', 'key3': 'val3'}, 'key4': {'key5': {'key6': 'val6'}}}
    False

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/oleg-golovanov/planedict/blob/master/LICENSE>`_ file for more details.
