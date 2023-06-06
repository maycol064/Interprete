import re
from typing import List

class Scanner:

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.line = 1
        self.reservedWords = {
            "and": "AND",
            "class": "CLASS",
            "else": "ELSE",
            "false": "FALSE",
            "for": "FOR",
            "fun": "FUN",  # define functions
            "if": "IF",
            "null": "NULL",
            "or": "OR",
            "print": "PRINT",
            "return": "RETURN",
            "super": "SUPER",
            "this": "THIS",
            "true": "TRUE",
            "var": "VAR",  # define variables
            "while": "WHILE",
        }

    def scanTokens(self):
        for match in re.finditer(r"([\w\s]+)|[(){}<>,.;+-*/!&=]", self.source):
            token_type = None
            lexeme = match.group(1)
            if lexeme in self.reservedWords:
                token_type = self.reservedWords[lexeme]
            else:
                if match.lastindex == 1:
                    token_type = "IDENTIFIER"
                elif match.lastindex == 2:
                    token_type = "LITERAL_STRING"
                elif match.lastindex == 3:
                    token_type = "LITERAL_NUMBER"
                else:
                    token_type = match.lastgroup
            self.tokens.append(Token(token_type, lexeme, None, self.line))
        self.line += self.source.count('\n')

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: List[Token] = []

    def generate_token(self, token_type: str, lexeme: str, literal: object, line: int) -> None:
        self.tokens.append(Token(token_type, lexeme, literal, line))

    def scan_tokens():
        state = 0
        start = 0
        nextState = 0
        c = ''
        lexeme = None
        literal = None
        source = source + ' '
        token_type = None
        tokens = []

        i = 0
        while i < len(source):
            c = source[i]
            if state == 0:
                if c == '_' or c.isalpha():
                    state = 10
                    nextState = i + 1
                elif c.isdigit():
                    state = 11
                    nextState = i + 1
                elif c == '<':
                    state = 1
                    nextState = i + 1
                elif c == '=':
                    state = 2
                    nextState = i + 1
                elif c == '>':
                    state = 3
                    nextState = i + 1
                elif c == '(':
                    generate_token(TipoToken.PARENT_OPEN, '(', None, line)
                    state = 0
                    start = nextState = i + 1
                elif c == ')':
                    generate_token(TipoToken.PARENT_CLOSE, ')', None, line)
                    state = 0
                    start = nextState = i + 1
                elif c == '{':
                    generate_token(TipoToken.BRACKET_OPEN, '{', None, line)
                    state = 0
                    start = nextState = i + 1
                elif c == '}':
                    generate_token(TipoToken.BRACKET_CLOSE, '}', None, line)
                    state = 0
                    start = nextState = i + 1
                elif c == ',':
                    generate_token(TipoToken.COMMA, ',', None, line)
                    state = 0
                    start = nextState = i + 1
                elif c == '.':
                    generate_token(TipoToken.DOT, '.', None, line)
                    state = 0
                    start = nextState = i + 1
                elif c == ';':
                    generate_token(TipoToken.SEMICOLON, ';', None, line)
                    state = 0
                    start = nextState = i + 1
                elif c == '-':
                    generate_token(TipoToken.LESS, '-', None, line)
                    state = 0
                    start = nextState = i + 1
                elif c == '+':
                    generate_token(TipoToken.GREAT, '+', None, line)
                    state = 0
                    start = nextState = i + 1
                elif c == '*':
                    generate_token(TipoToken.MULT, '*', None, line)
                    state = 0
                    start = nextState = i + 1
                elif c == '/':
                    state = 4
                    nextState = i + 1
                elif c == '"':
                    state = 8
                    nextState = i + 1
                elif c == '!':
                    state = 9
                    nextState = i + 1
                elif c.isspace():
                    state = 17
                    i += 1
                    if c == '\n':
                        line += 1
                else:
                    Interprete.error(line, "Unrecognized character.")
                    start = nextState = i + 1
                    state = 0
            elif state in [1, 2, 3]:
                if c == '=':
                    nextState = i + 1
                    lexeme = source[start:nextState]
                    if lexeme == "<=":
                        generate_token(TipoToken.LESS_EQUAL, "<=", None, line)
                    elif lexeme == "==":
                        generate_token(TipoToken.EQUAL, "==", None, line)
                    else:
                        generate_token(TipoToken.GREAT_EQUAL, ">=", None, line)
                    state = 0
                    start = i
                else:
                    lexeme = source[start:nextState]
                    if lexeme == "<":
                        generate_token(TipoToken.LESS_THAN, "<", None, line)
                    elif lexeme == "=":
                        generate_token(TipoToken.ASIGNATION, "=", None, line)
                    else:
                        generate_token(TipoToken.GREAT_THAN, ">", None, line)
                    state = 0
                    nextState = start = i
            elif state == 4:
                if c == '/':
                    state = 5
                    nextState = i + 1
                elif c == '*':
                    state = 6
                    nextState = i + 1
                else:
                    generate_token(TipoToken.SLASH, "/", None, line)
                    state = 0
                    start = nextState = i
                    break
            elif state == 5:
                if c == '\n':
                    state = 0
                    start = nextState = i + 1
                else:
                    state = 5
                    i += 1
            elif state == 6:
                if i == len(source):
                    Interprete.error(line, "Expected end of comment.")
                    i += 1
                    break
                if c == '\n':
                    line += 1
                if c == '*':
                    state = 7
                else:
                    state = 6
                nextState = i + 1
            elif state == 7:
                if i == len(source):
                    Interprete.error(line, "Expected '/'.")
                    i += 1
                    break
                if c == '/':
                    state = 0
                    start = nextState = i + 1
                else:
                    state = 6
                    i += 1
            elif state == 8:
                if i == len(source):
                    Interprete.error(line, "Expected '\"'.")
                    i += 1
                    break
                if c == '"':
                    lexeme = source[start:nextState + 1]
                    literal = source[start + 1:nextState]
                    generate_token(TipoToken.STRING, lexeme, literal, line)
                    state = 0
                    start = nextState = i + 1
                else:
                    state = 8
                    nextState = i + 1
            elif state == 9:
                if c == '=':
                    generate_token(TipoToken.DIFERENT, "!=", None, line)
                    state = 0
                    start = nextState = i + 1
                else:
                    generate_token(TipoToken.NEGATION, "!", None, line)
                    state = 0
                    start = nextState = i
            elif state == 10:
                if c == '_' or c.isalpha() or c.isdigit():
                    state = 10
                    nextState = i + 1
                else:
                    lexeme = source[start:nextState]
                    token_type = palabras_reservadas.get(lexeme, TipoToken.IDENTIFIER)
                    generate_token(token_type, lexeme, None, line)
                    state = 0
                    start = nextState = i
            elif state == 11:
                if c.isdigit():
                    state = 11
                    nextState = i + 1
                elif c == '.':
                    state = 12
                    nextState = i + 1
                elif c == 'E':
                    state = 14
                    nextState = i + 1
                else:
                    lexeme = source[start:nextState]
                    num = float(lexeme)
                    generate_token(TipoToken.NUMBER, lexeme, num, line)
                    state = 0
                    start = nextState = i
            elif state == 12:
                if c.isdigit():
                    state = 13
                    nextState = i + 1
                else:
                    Interprete.error(line, "Expected a number.")
                    lexeme = source[start:nextState - 1]
                    num = float(lexeme)
                    generate_token(TipoToken.NUMBER, lexeme, num, line)
                    state = 0
                    start = nextState = i - 1
            elif state == 13:
                if c.isdigit():
                    state = 13
                    nextState = i + 1
                elif c == 'E':
                    state = 14
                    nextState = i + 1
                else:
                    lexeme = source[start:nextState]
                    num = float(lexeme)
                    generate_token(TipoToken.NUMBER, lexeme, num, line)
                    state = 0
                    start = nextState = i
            elif state == 14:
                if c == '+' or c == '-':
                    state = 15
                    nextState = i + 1
                elif c.isdigit():
                    state = 16
                    nextState = i + 1
                else:
                    Interprete.error(line, "Expected a number, '+' or '-'.")
                    lexeme = source[start:nextState - 1]
                    num = float(lexeme)
                    generate_token(TipoToken.NUMBER, lexeme, num, line)
                    state = 0
                    start = nextState = i - 1
            elif state == 15:
                if c.isdigit():
                    state = 16
                    nextState = i + 1
                else:
                    Interprete.error(line, "Expected a number.")
                    lexeme = source[start:nextState - 2]
                    num = float(lexeme)
                    generate_token(TipoToken.NUMBER, lexeme, num, line)
                    state = 0
                    i -= 2
                    start = nextState = i
            elif state == 16:
                if c.isdigit():
                    state = 16
                    nextState = i + 1
                else:
                    lexeme = source[start:nextState]
                    num = float(lexeme)
                    generate_token(TipoToken.NUMBER, lexeme, num, line)
                    state = 0
                    start = nextState = i
            elif state == 17:
                if c.isspace():
                    state = 17
                    i += 1
                    if c == '\n':
                        line += 1
                else:
                    state = 0
                    start = nextState = i
        generate_token(TipoToken.EOF, "", None, line)
        return tokens
