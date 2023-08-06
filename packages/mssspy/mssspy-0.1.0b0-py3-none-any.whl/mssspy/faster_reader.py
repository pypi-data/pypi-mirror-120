"""Implements the slightly faster (but still pure-Python `FasterReader`)."""


import mmap
from types import TracebackType
from typing import Optional, Type

import numpy as np  # type: ignore

from . import Sample
from .slow_reader import SlowReader


class FasterReader(SlowReader):
    """
    Similar to `SlowReader` (and still pure-Python) but a bit faster (about
    2x).

    This reader makes many concessions in terms of checking correctness of the
    input file, and assumes correctly-formatted ms files.  It may crash in
    unexpected ways when encountering a malformatted file, or a malformatted
    sample within an otherwise correct file.

    This reader should be preferred by default over `SlowReader`, though
    `SlowReader` can be fallen back on in order to better handle problems in
    poorly-formatted inupt files.
    """

    name = 'faster'

    def __enter__(self) -> 'FasterReader':
        super().__enter__()
        if self._opencount == 1:
            self._orig_fd = self._fd
            self._fd = mmap.mmap(self._fd.fileno(), 0, flags=mmap.MAP_PRIVATE)
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        if self._opencount == 1:
            self._fd.close()
            self._fd = self._orig_fd
            self._orig_fd = None
        super().__exit__(exc_type, exc_val, exc_tb)

    def _parse_sample(self, idx: int) -> Sample:
        positions = None
        haplotypes = None

        # For the fast reader actually we ignore the segsites line entirely
        # since we can infer it from the positions list (I don't think there's
        # ever a time they won't be the same, based on the original ms.c
        # source)

        while True:
            start = self._fd.tell()
            line = self._fd.readline()

            if not line:
                break

            first_char = line[:1]

            if first_char == b'p':  # for positions:
                positions = np.fromstring(line[11:-1], sep=' ')
            elif first_char in (b'0', b'1'):
                # We can infer the number of positions from the length of the
                # line
                n_pos = len(line) - 1
                # In the haplotypes block; find the end of it by finding the
                # next double-newline or EOF
                end = self._fd.find(b'\n\n', start) + 1
                end = end if end > start else self._fd.size()
                # We can infer the number of haplotypes by the size of the
                # block
                n_hap = (end - start) // (n_pos + 1)
                shape = (n_hap, n_pos)
                haplotypes = np.ndarray(shape, buffer=self._fd[start:end],
                                        strides=(n_pos + 1, 1),
                                        dtype=np.uint8) - ord(b'0')
                break
            elif first_char == b'\n':
                # We reached a blank line, so this should be the end of the
                # sample
                break

        if positions is None:
            # Some samples, if nsamps is low, can have segsites: 0 and no
            # positions section
            positions = np.array([], dtype=float)

        if haplotypes is None:
            # Something else unrecognized or start of another sample
            haplotypes = np.array([], dtype=np.uint8)

        return Sample(haplotypes, positions)
