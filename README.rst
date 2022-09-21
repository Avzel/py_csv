=======
py_csv
=======

Provides a stateful API for streaming individual CSV rows
as Python dictionaries from column name to value.

Follows the RFC4180 specification for CSV files,
and always expects a header on row 0.

Identifies format errors and provides the location 
and type of error **(values start at 1)**

Parses CSV files character by character and without backtracking,
so will read the entire file in linear O(N) time.

Running
========

**NOTE**: Requires Python 3.10+, no external dependencies

+ Ensure the `py_csv` package is in your project and import `from py_csv.csv_parser import CSVParser`

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
