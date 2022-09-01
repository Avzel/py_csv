from enum import Enum


class State(Enum):

    START       = object()
    QUOTED      = object()
    FREE        = object()
    END         = object()

class Type(Enum):

    NONE        = object()
    LF          = object()
    CR          = object()
    SQ          = object()
    FQ          = object()
    COMMA       = object()
    TEXTDATA    = object()
