from enums import State, Type
from exceptions import CSVParseException
from io import StringIO
from typing import Union


class CSVParser:
    '''
    Provides a stateful API for streaming individual 
    CSV rows as dict() from column name to value

    ...

    Public Methods
    --------------
    __init__(filename: str)
        constructor takes a filename and opens a TextIOWrapper for reading
    set_file(filename: str) -> None
        opens a TextIOWrapper for reading with the given filename
    read_row() -> dict<str, str> or None
        returns a single row as a dict<str, str> on each call
        until EOF, at which point returns None
    reset() -> None
        resets the CSVParser object so it can be used again
    '''

    def __init__(self, filename: Union[str, None]=None) -> None:
        '''
        Constructs a CSVParser object
        
        ...
        
        Parameters
        ----------
        filename: str
            the filename for opening a TextIOWrapper for reading
        '''

        # CSV file object for reading
        self.__file           = open(filename, 'r') if filename else None

        # holds a single CSV field
        self.__field          = StringIO()
        # holds all fields in a single row
        self.__fields         = list()
        # holds all column names in order
        self.__headers        = list()
        # holds all column names mapped to their fields in a single row
        self.__entry          = dict()

        # represents the state of the reader
        self.__state          = State.START
        # represents the char type of the previously read character
        self.__prev           = Type.NONE

        # current row number
        self.__row            = 1
        # current line number
        self.__line           = 1
        # current column number
        self.__column         = 1
        # total number of columns
        self.__total_columns  = 0
        # whether the reader has encountered EOF
        self.__end            = False

    def set_file(self, filename: str) -> None:
        '''
        Opens a TextIOWrapper for reading with the given filename

        ...

        Parameters
        ----------
        filename : str
            file name for opening a TextIOWrapper for reading
        '''

        if self.__file:
            self.reset()

        self.__file = open(filename, 'r')

    def read_row(self) -> Union[dict[str, str], None]:
        '''
        Returns a single row of the CSV file as a dict<str, str>
        on each call until EOF, at which point returns None

        ...

        Returns
        -------
        dict<str, str> : single row of CSV file as dict from column name to value
        None : when the reader encounters EOF

        Raises
        ------
        py_csv.exceptions.CSVParseException : if the CSV file is formatted incorrectly
        '''

        if self.__end:
            self.reset()
            return None

        while char := self.__file.read(1):
            match char:

                case '\n':

                    if self.__state in [State.START, State.END, State.FREE] or \
                            (self.__state == State.QUOTED and self.__prev == Type.FQ):

                        self.__finalize_row()
                        if self.__entry: return self.__entry
                        else: continue

                    elif self.__state == State.QUOTED:
                        self.__field.write(char)
                        self.__line += 1
                        self.__column = 1
                        self.__prev = Type.LF

                case '\r':
                    match self.__state:

                        case State.START | State.FREE:
                            self.__state = State.END
                            self.__prev = Type.CR

                        case State.END:
                            self.__raise_parse_exception(
                                "ERROR: double carriage return")

                        case State.QUOTED:
                            if self.__prev == Type.FQ: self.__state = State.END
                            else: self.__field.write(char)
                            self.__prev = Type.CR

                case '"':
                    match self.__state:

                        case State.START:
                            self.__check_field_count()
                            self.__state = State.QUOTED
                            self.__prev = Type.SQ

                        case State.END:
                            self.__raise_parse_exception(
                                "ERROR: end-of-row carriage feturn followed by a quote instead of line feed")

                        case State.FREE:
                            self.__raise_parse_exception(
                                "ERROR: quote in a non-quoted field")

                        case State.QUOTED:
                            if self.__prev == Type.FQ:
                                self.__field.write(char)
                                self.__prev = Type.TEXTDATA
                            else:
                                self.__prev = Type.FQ

                case ',':
                    if self.__state in [State.START, State.FREE] or \
                            (self.__state == State.QUOTED and self.__prev == Type.FQ):

                        self.__append_field()
                        self.__clear_field()
                        self.__state = State.START
                        self.__prev = Type.COMMA

                    elif self.__state == State.QUOTED:
                        self.__field.write(char)
                        self.__prev = Type.TEXTDATA

                    elif self.__state == State.END:
                        self.__raise_parse_exception(
                            "ERROR: end-of-row carriage return followed by a comma instead of line feed")

                case _:
                    if self.__state == State.START or \
                            (self.__state in [State.FREE, State.QUOTED] and self.__prev != Type.FQ):

                        self.__check_field_count()
                        self.__field.write(char)
                        self.__prev = Type.TEXTDATA

                        if self.__state == State.START: self.__state = State.FREE

                    elif self.__state in [State.FREE, State.QUOTED]:
                        self.__raise_parse_exception(
                            "ERROR: single quote followed by text data in a quoted field")

                    elif self.__state == State.END:
                        self.__raise_parse_exception(
                            "ERROR: end-of-row carriage return followed by text data instead of line feed")

            self.__column += 1

        if self.__column != 1:
            self.__end = True
            self.__finalize_row()
            return self.__entry
        else:
            self.reset()
            return None

    def __check_field_count(self):

        if self.__total_columns and len(self.__fields) >= self.__total_columns:
            self.__raise_parse_exception(
                "ERROR: column number mismatch")

    def __append_field(self) -> None:

        self.__fields.append(self.__field.getvalue())

    def __finalize_row(self) -> None:

        self.__append_field()

        if self.__row == 1: self.__set_headers()
        else: self.__set_entry()

        self.__prepare_next_row()

    def __set_headers(self) -> None:

        self.__total_columns = len(self.__fields)

        for field in self.__fields:
            self.__headers.append(field)

    def __set_entry(self) -> None:

        self.__entry.clear()

        for i in range(0, self.__total_columns):
            self.__entry[self.__headers[i]] = self.__fields[i]

    def __raise_parse_exception(self, message: str) -> None:

        raise CSVParseException(
            message, 
            self.__line, 
            self.__row, 
            self.__column, 
            len(self.__fields) + 1)

    def __clear_field(self) -> None:

        self.__field.close()
        self.__field = StringIO()

    def __prepare_next_row(self) -> None:

        self.__clear_field()
        self.__fields.clear()

        self.__state = State.START
        self.__prev = Type.NONE

        self.__row += 1
        self.__line += 1
        self.__column = 1

    def reset(self) -> None:
        '''
        Resets the CSVParser object so it can be used again

        Call this.set_file() to reinitialize the reader after calling this.reset()
        '''

        self.__file.close()
        self.__end = False

        self.__clear_field()
        self.__fields.clear()
        self.__entry.clear()

        self.__state = State.START
        self.__prev = Type.NONE

        self.totalColumns = 0
        self.__row = 1
        self.__line = 1
        self.__column = 1
