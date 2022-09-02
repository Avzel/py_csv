=======
py_csv
=======

Provides a stateful API for streaming individual CSV rows
as Python dictionaries from column name to value.

Parses CSV files character by character and without backtracking,
so will read the entire file in linear O(N) time.

Follows the RFC4180 specification for CSV files,
except that it always expects a header on row 0.

Building
========

Requires Python 3.10+
