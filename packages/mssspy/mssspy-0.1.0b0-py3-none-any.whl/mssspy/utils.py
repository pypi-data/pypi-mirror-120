"""Miscellaneous utilities."""


import itertools
import timeit
from collections import OrderedDict


class LRUDict(OrderedDict):
    """
    `dict` which keeps up to ``maxsize`` of the most recently accessed entries.

    It is based on `collections.OrderedDict` due to its optimization for
    reordering.

    Examples
    --------

    >>> from renewal_backend.utils import LRUDict
    >>> d = LRUDict({'a': 1, 'b': 2}, maxsize=2)
    >>> d['b']
    2
    >>> d['c'] = 3
    >>> d
    LRUDict([('b', 2), ('c', 3)])
    >>> d['b']
    2
    >>> d['d'] = 4
    >>> d
    LRUDict([('b', 2), ('d', 4)])

    You can also change ``maxsize`` at runtime: If smaller than the previous
    ``maxsize`` this will cause trucation of the least recent entries:

    >>> d.maxsize = 1
    >>> d
    LRUDict([('d', 4)])

    You may also set ``maxsize = None`` which disables the LRU feature and
    allows it to work as a normal `dict` until/unless ``maxsize`` is set again.
    """

    def __init__(self, *args, maxsize=128, **kwargs):
        self.maxsize = maxsize
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)

        # Delete old keys until we are down to maxsize
        self._truncate()

    @property
    def maxsize(self):
        return self._maxsize

    @maxsize.setter
    def maxsize(self, maxsize):
        assert maxsize is None or maxsize > 0
        self._maxsize = maxsize
        self._truncate()

    def _truncate(self):
        if self._maxsize is not None:
            while len(self) > self._maxsize:
                del self[next(iter(self))]


def timings(filename, reader, indices=None, with_index=False,
            with_cache=False):
    """
    Utility function to test performance of difference readers.

    .. todo::

        Additional documentation of this function in case anyone wants to use
        it to test their own readers.
    """

    from . import MSReader

    if isinstance(reader, str):
        # The .name of the reader is provided, otherwise we assume reader is an
        # MSReader subclass
        reader = MSReader.registry[reader]

    # If indices=None we just test on all indices until we get one with an
    # index error.  To test this (before running the timings) we call the
    # reader directly to see if raises an IndexError on the given index.
    # Otherwise, if the list of indices is provided explicitly, we test even
    # those that might not exist.
    test_reader = reader(filename)

    if indices is None:
        indices = itertools.count()
        check_valid_index = True
    else:
        check_valid_index = False

    # If testing with_cache=True we test calls through the MSFile interface
    # which provides the caching mechanism.  Otherwise we test calls directly
    # through the reader.  This determins the setup and statement codes to pass
    # to timeit.
    # with_cache also necessarily implies with_index regardless what was passed
    # for the with_index option.
    #
    # In both cases we call MSFile/MSReader.__enter__() in the setup code so
    # that the overhead of opening the file is not included in the test.
    if with_cache:
        setup = (f'import mssspy; '
                 f'f = mssspy.MSFile({repr(filename)}, '
                 f'                  reader={repr(reader.name)}); '
                 f'f.__enter__()')
        stmt = 'x = f[{idx}]'
    else:
        setup = (f'import mssspy; '
                 f'cls = mssspy.MSReader.registry[{repr(reader.name)}]; '
                 f'r = cls({repr(filename)}, index={with_index}); '
                 f'r.__enter__()')
        stmt = 'x = r.read_sample({idx})'

    tested_indices = []
    timings = []

    for idx in indices:
        if check_valid_index:
            try:
                test_reader.get_sample(idx)
            except IndexError:
                break

        tested_indices.append(idx)
        timer = timeit.Timer(setup=setup, stmt=stmt.format(idx=idx))
        number, _ = timer.autorange()
        repeat_timings = timer.repeat(number=number)
        timings.append(min(repeat_timings) / number)

    return tested_indices, timings
