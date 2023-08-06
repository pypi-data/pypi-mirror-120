"""mssspy -- A Python reader for ms/msms files"""


import inspect
import io
import os
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import (Any, AnyStr, Dict, Hashable, IO, List, Optional, Tuple,
                    Type, Union, cast)
from warnings import warn

import numpy as np  # type: ignore

from .utils import LRUDict


# Typing aliases
ReaderArg = Union[str, Type['MSReader']]


class MssspyWarning(UserWarning):
    """Warnings from `mssspy`."""


class ParseError(Exception):
    """Error in parsing of ms files."""


@dataclass
class Sample:
    haplotypes: np.ndarray
    positions: np.ndarray

    @property
    def segsites(self) -> int:
        """Number of polymorphic sites in the sample."""

        return len(self.positions)


class Index(list):
    complete: bool
    path: Optional[str]

    def __new__(cls, offsets: List[int] = [], complete: bool = False,
                path: Optional[str] = None) -> 'Index':
        # typing: typeshed is missing the correct stubs for list.__new__()
        # it should have been added in this PR, perhaps, but was not and is
        # still missing: https://github.com/python/typeshed/pull/4555/files
        # Surprised this hasn't come up for anyone else...
        self = super().__new__(cls, offsets)  # type: ignore
        self.complete = complete
        self.path = path
        return self


class MSReader(metaclass=ABCMeta):
    """
    Base class for lower-level ``ms`` file readers.

    This can have multiple implementations with different advantages or
    optimizations depending on your needs.  This also allows extending `mssspy`
    with custom readers.
    """

    registry: Dict[str, Type['MSReader']] = {}
    name: str

    def __init__(self, data_source: Any,
                 index: Optional[Union[Index, bool]] = None) -> None:
        """
        Initialize the reader with a data source which may be any arbitrary
        object, though typically it will be an open file-like object.

        Typically this will be a file-like object or something similar.
        """

        self.data_source = data_source

        if index in (None, True):
            index = Index()
        elif index is False:
            index = None

        self.index = cast(Optional[Index], index)

    def __init_subclass__(cls: Type['MSReader']) -> None:
        """Add this reader to the registry of available readers."""

        try:
            cls.name
        except AttributeError:
            # This is necessary since "abstract class attributes" are not
            # really supported by the abc module or by mypy
            if not inspect.isabstract(cls):
                raise RuntimeError(
                    f'concrete implementations of MSReader require a name '
                    f'attribute')
        else:
            if cls.name in cls.registry:
                warn(f'an MSReader named {cls.name} already exists in '
                     f'{cls.registry[cls.name].__module__} and will be '
                     f'replaced by {cls.__module__}.{cls.__qualname__}',
                     MssspyWarning)

            cls.registry[cls.name] = cls

    def __enter__(self) -> 'MSReader':
        """
        Dummy ``__enter__`` method so the reader can be used as a context
        manager.  Implement this and/or ``__exit__`` to manage resources
        (e.g. when the ``data_source`` is a file to be opened/closed).

        It should return ``self``.
        """

        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        """
        Dummy ``__exit__`` method so the reader can be used as a context
        manager.  Implement this and or ``__enter__`` to manage resources
        (e.g. when the ``data_source`` is a file to be opened/closed).
        """

    @abstractmethod
    def read_sample(self, idx: int = 0, index_only: bool = False) -> Sample:
        """
        Read the N-th sample in the file.

        By default the first (0th) sample is read, in the case of single-sample
        files.
        """

    @classmethod
    def cache_key(cls, data_source: Any) -> Hashable:
        """
        For a given instance of the ``data_source`` accepted by this reader,
        return a hashable key used to cache the data source's index.

        For example, given a filename, this might return the pair ``(filename,
        mtime)`` for the file.

        If it cannot generate a cache key for the given ``data_source``, this
        should raise `NotImplementedError`, and the data source's index cannot
        be cached.
        """

        raise NotImplementedError(
            f'the data source {data_source} does not have a cacheable index')

    @classmethod
    def get(cls, name: str) -> Type['MSReader']:
        """Get an `MSReader` subclass by name."""

        try:
            return cls.registry[name]
        except KeyError:
            raise ValueError(
                f'unknown reader: {name}; available readers are: '
                f'{list(cls.registry)}')



class FileReader(MSReader):
    """
    Base class for readers that read from a filesystem path or file-like
    object.

    This base class handles details such as opening/closing files, as well as
    generating the cache key.  Index caching is currently only possible for
    files with filesystem paths.

    The details of actually reading and parsing the file are left to individual
    implementations.
    """

    def __init__(self, data_source: Union[str, Path, IO[AnyStr]],
                 index: Optional[Index] = None) -> None:
        super().__init__(data_source, index)
        self._fd: Optional[IO] = None
        self._closefd = False
        self._opencount = 0

        if self.index is not None and isinstance(data_source, (str, Path)):
            self.index.path = str(data_source)

    def __enter__(self) -> 'FileReader':
        if self._opencount == 0:
            if isinstance(self.data_source, (str, Path)):
                self._fd = open(self.data_source, 'rb')
                self._closefd = True
            else:
                self._fd = self.data_source

        # Allows enter/exit to be re-entrant
        self._opencount += 1
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        self._opencount -= 1
        if self._opencount == 0 and self._closefd and self._fd is not None:
            self._fd.close()

    @classmethod
    def cache_key(cls, data_source: Union[str, Path, IO[AnyStr]]) -> Tuple[str, float]:
        if isinstance(data_source, io.FileIO):
            # typing: here data_source.name could also be an int, but we use
            # the cast to ignore that case, do an explicit isinstance check
            # below
            name = cast(Union[str, Path], data_source.name)
        else:
            name = cast(Union[str, Path], data_source)

        if isinstance(name, (str, Path)):
            mtime = os.stat(name).st_mtime
            return (str(name), mtime)

        return super().cache_key(data_source)


class MSFile:
    """
    High-level interface for ms files.

    When a file is opened, individual samples in the file can be accessed by
    indexing the `MSFile` instance.

    Actual reading of the file is delegated to the chosen reader.

    This class also implements caching of "indices" for files in the most
    common cases (e.g. files on disk), which allow rapid access to individual
    samples within a file without having to fully re-parse them.
    """

    _index_cache: LRUDict = LRUDict(maxsize=None)
    """Global index cache."""

    reader: MSReader
    fallback_reader: Optional[MSReader]

    def __init__(self, path_or_obj: Any,
                 reader: ReaderArg = 'faster',
                 disable_index_cache: bool = False,
                 fallback_reader: Optional[ReaderArg] = None) -> None:
        self.path_or_obj = path_or_obj

        if isinstance(reader, str):
            reader = MSReader.get(reader)

        if isinstance(fallback_reader, str):
            fallback_reader = MSReader.get(fallback_reader)

        # Reader should now be an MSReader subclass
        reader = cast(Type[MSReader], reader)
        fallback_reader = cast(Optional[Type[MSReader]], fallback_reader)

        if not disable_index_cache:
            index = self._cached_index(reader, path_or_obj)
        else:
            index = None

        self.reader = reader(path_or_obj, index=index)

        # If using a FileReader other than SlowReader, construct a SlowReader
        # as the default fallback
        if (fallback_reader is None and issubclass(reader, FileReader) and
                reader is not SlowReader):
            fallback_reader = SlowReader

        if fallback_reader is not None:
            self.fallback_reader = fallback_reader(path_or_obj, index=index)
        else:
            self.fallback_reader = None

    def __enter__(self) -> 'MSFile':
        # Delegate to the underlying reader's __enter__
        self.reader.__enter__()
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        # Delegate to the underlying reader's __exit__
        self.reader.__exit__(exc_type, exc_val, exc_tb)

    def __getitem__(self, idx: int) -> Sample:
        try:
            return self.reader.read_sample(idx)
        except IndexError:
            raise
        except Exception as exc:
            if self.fallback_reader is not None:
                warn(
                    f'{self.reader.name} reader failed on sample {idx} of '
                    f'{self.path_or_obj} ({exc}); '
                    f'trying {self.fallback_reader.name} as a fallback',
                    MssspyWarning)
                return self.fallback_reader.read_sample(idx)
            else:
                raise

    @classmethod
    def resize_index_cache(cls, size: Optional[int]) -> None:
        """
        Set the maximum size (in number of files) of the cache of file indices.

        By default the size of the cache is unbounded.  Setting a smaller size
        will cause the cached indices of less recently used files to be
        dropped.
        """

        cls._index_cache.maxsize = size

    @classmethod
    def _cached_index(cls, reader: Type[MSReader],
                      path_or_obj: Any) -> Optional[Index]:
        try:
            cache_key = reader.cache_key(path_or_obj)
        except NotImplementedError:
            cache_key = None

        if cache_key is not None:
            try:
                index = cls._index_cache[cache_key]
            except KeyError:
                # No index cache available for this file
                index = Index()
                cls._index_cache[cache_key] = index
        else:
            index = None

        return index


# Import and register the built-in readers
from .slow_reader import SlowReader  # noqa: E402
from .faster_reader import FasterReader  # noqa: E402, F401
