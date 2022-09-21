class CSVParseException(Exception):

    def __init__(self, message, line, row, column, field):
        '''
        Prints an error message providing the line, row, column, 
        and field numbers where the formatting error was encountered, 
        as well as a custom given message

        Stores the given line, row, column, and field numbers as
        instance variables
        
        All values count from 1

        Parameters & Fields
        -------------------
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

        self.line = line
        self.row = row
        self.column = column
        self.field = field
        
        self.message = f"CSV parsing error (line {line}, row {row}, column {column}, field {field}): {message}"

        super().__init__(self.message)
