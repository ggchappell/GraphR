GraphR
======

Python code for dealing with finite, simple graphs. Allows for
computation of generalized Ramsey numbers and associated extremal
graphs. Requires Python 2.6.* or 2.7.*.

This package is a companion to the following papers by Glenn G. Chappell
and John Gimbel:
* On defective Ramsey numbers
* On subgraphs without large components

See the papers for mathematical background and related results.

Package repository: <https://github.com/ggchappell/GraphR>

Copyright & License
-------------------

Package copyright &copy; 2013-2016 Glenn G. Chappell.

License: MIT. See [`LICENSE`](LICENSE) or
<http://opensource.org/licenses/MIT>.

Usage
-----

In its current form, GraphR requires that the user be at least somewhat
familiar with Python and use of the command line.

GraphR consists of two executable programs (`sparseramsey.py`,
`dividedramsey.py`) and two importable libraries used by these
(`isograph.py`, `genramsey.py`). All are intended for use with Python
2.6.* or 2.7.*.

To compute the _sparse Ramsey number_ R_k(a, b), run `sparseramsey.py`,
passing k, a, b as command-line arguments.

    > sparseramsey.py 2 5 7

To compute the _divided Ramsey number_ R*_k(a, b), run
`dividedramsey.py`, passing k, a, b, as command-line arguments.

    > dividedramsey.py 4 5 6

All four files may be used as importable modules. See the individual
files for API documentation. Data formats are described in
`isograph.py`.

Files
-----

* `isograph.py` -- Importable module. Functions for dealing with simple
  graphs & graph isomorphism.
* `genramsey.py` -- Importable module. Functions for finding generalized
  Ramsey numbers & related extremal graphs. Requires `isograph.py`.
* `sparseramsey.py` -- Executable program/importable module. Computes
  sparse Ramsey numbers. Requires `isograph.py` and `genramsey.py`.
* `dividedramsey.py` -- Executable program/importable module. Computes
  divided Ramsey numbers. Requires `isograph.py` and `genramsey.py`.
* `RESULTS` -- Subdirectory for text files holding output of
  `sparseramsey.py` or `dividedramsey.py`. Files named `r##_##_##.txt`,
  where `#` represents a digit, hold output from `sparseramsey.py`. The
  numbers in the filename are the command-line parameters. For example,
  file `r02_05_06.txt` holds the output from the command
  `sparseramsey.py 2 5 6`. Similarly, files named `rs##_##_##.txt` hold
  output from `dividedramsey.py`.
* `README.md` -- This file.
* `LICENSE` -- Package license.

