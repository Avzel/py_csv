from enum import Enum


class State(Enum):

    START       = object()  # The start of a field
    QUOTED      = object()  # In the middle of parsing a quoted field
    FREE        = object()  # In the middle of parsing a non-quoted field
    END         = object()  # At the end of the row

class Type(Enum):

    NONE        = object()
    LF          = object()
    CR          = object()
    SQ          = object()  # "Starting Quote" - double quote not preceded by a double quote
    FQ          = object()  # "Following Quote" - double quote preceded by a double quote
    COMMA       = object()
    TEXTDATA    = object()  # Anything else
