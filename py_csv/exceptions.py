class ParseException(Exception):

    def __init__(self, message, line, row, column, field):
        '''
        Prints an error message providing the line, row, column, 
        and field numbers where the formatting error was encountered, 
        as well as a custom given message
        
        Parameters
        ----------
        message: str
            the custom message to be printed after the base message
        line: int
            the line number on which the formatting error was encountered
        row: int
            the row number at which the formatting error was encountered
        column: int
            the column number at which the formatting error was encountered
        field: int
            the field number in which the formatting error was encountered
        '''

        print(f"Parsing error (line {line}, row {row}, column {column}, field {field}): {message}")
