from enum import Enum

class TokenType(Enum):
    AND ="and"
    CLASS = "class"
    ALSO = "also"
    FALSE = "false"
    FOR = "for"
    FUN = "fun"
    IF = "if"
    NULL = "null"
    OR = "or"
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "var"
    WHILE = "while"
    EOF = "EOF"
    #Signos o símbolos del lenguaje:
    OPENPARENT = "("
    CLOSEPARENT = ")"
    OPENBRACKET = "{"
    CLOSEBRACKET = "}"
    COMMA = ","
    DOT = "."
    DOTCOMMA = ";"
    SUB = "-"
    ADD = "+"
    MULT = "*"
    DIVID = "/"
    NEGATION = "!"
    DIFFERENT = "!="
    ASIGNATION = "="
    EQUAL = "=="
    LESS = "<"
    LESSEQUAL = "<="
    GREAT = ">"
    GREATEQUAL = ">="
    COMMENT = "//" # -> comentarios (no se genera token)
    MULTCOMMENT = "/* ... * /"  #-> comentarios (no se genera token)
    NUMBER = "NUM"
    IDENTIFIER = "ID"
    #Identificador,
    #Cadena
    #Numero
    #Cada palabra reservada tiene su nombre de token