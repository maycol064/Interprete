from enum import Enum


class TokenType(Enum):
    """A token type in a programming language."""

    # Identifier, string, and number
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"

    # Keywords
    AND = "AND"
    CLASS = "CLASS"
    ELSE = "ELSE"
    FALSE = "FALSE"
    FOR = "FOR"
    FUN = "FUN"
    IF = "IF"
    NULL = "NULL"
    OR = "OR"
    PRINT = "PRINT"
    RETURN = "RETURN"
    SUPER = "SUPER"
    THIS = "THIS"
    TRUE = "TRUE"
    VAR = "VAR"
    WHILE = "WHILE"

    # Symbols
    PARENT_OPEN = "PARENT_OPEN"
    PARENT_CLOSE = "PARENT_CLOSE"
    BRACKET_OPEN = "BRACKET_OPEN"
    BRACKET_CLOSE = "BRACKET_CLOSE"
    COMMA = "COMMA"
    DOT = "DOT"
    SEMICOLON = "SEMICOLON"
    LESS = "LESS"
    GREAT = "GREAT"
    MULT = "MULT"
    NEGATION = "NEGATION"
    DIFERENT = "DIFERENT"
    ASIGNATION = "ASIG"
    EQUAL = "EQUAL"
    LESS_THAN = "LESS_THAN"
    LESS_EQUAL = "LESS_EQUAL"
    GREAT_THAN = "GREAT_THAN"
    GREAT_EQUAL = "GREAT_EQUAL"
    SLASH = "SLASH"

    # End of string
    EOF = "EOF"

