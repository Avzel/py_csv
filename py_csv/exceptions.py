class ParseException(Exception):

    def __init__(self, message, line, row, column, field):

        print(f"Parsing error (line {line}, row {row}, column {column}, field {field}): {message}")