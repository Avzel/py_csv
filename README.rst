=======
py_csv
=======

Provides a stateful API for streaming individual CSV rows
as Python dictionaries from column name to value.

Parses CSV files character by character and without backtracking,
so will read the entire file in linear O(N) time.

Follows the RFC4180 specification for CSV files,
except that it always expects a header on row 0.

Running
========

**NOTE**: Requires Python 3.10+

+ Ensure the `py_csv` package is in your project and import `csv_parser`

+ Call `CSVParser()` to create a reader object

+ Either provide the filename during construction as `CSVParser(filename)` 
or call `set_file(filename)` on the reader object

+ Call `read_row()` on the reader object to read rows one at a time

+ After reaching EOF, the reader will automatically reset, 
allowing you to call `set_file(filename)` again on another file

+ You can also manually reset the reader with a `reset()` call on the object

Coming Soon
============

+ PyPI package
