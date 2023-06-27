import re
from tokenType import TokenType
from tokens import Token
import string  # Importar el módulo string


class Scanner:  # Clase Scanner
    def __init__(self, source) -> None: 
        self.source = source
        self.line = 1
        self.tokens = []
        self.reserved_words = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "also": TokenType.ALSO,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "null": TokenType.NULL,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
            "else": TokenType.ELSE,
        }

    def scanTokens(self) -> list[Token]:
        self.state = 0
        for line in self.source:
            current = ""
            line1 = self.clean(line)
            line1 += " "
            for char in line1:
                match self.state:
                    case 0:
                        if char == "<":
                            self.state = 1
                        elif char == "=":
                            self.state = 2
                        elif char == ">":
                            self.state = 3
                        elif char.isdigit():
                            current += char
                            self.state = 4
                        elif char.isalpha():
                            current += char
                            self.state = 5
                        elif char == "/":
                            self.state = 6
                        elif char == "{":
                            self.tokens.append(
                                Token(TokenType.BRACKET_OPEN, "{", None, self.line)
                            )
                            self.state = 0
                        elif char == "}":
                            self.tokens.append(
                                Token(TokenType.BRACKET_CLOSE, "}", None, self.line)
                            )
                            self.state = 0
                        elif char == "(":
                            self.tokens.append(
                                Token(TokenType.PARENT_OPEN, "(", None, self.line)
                            )
                            self.state = 0
                        elif char == ")":
                            self.tokens.append(
                                Token(TokenType.PARENT_CLOSE, ")", None, self.line)
                            )
                            self.state = 0
                        elif char == "+":
                            self.tokens.append(
                                Token(TokenType.SUB, "+", None, self.line)
                            )
                            self.state = 0
                        elif char == "-":
                            self.tokens.append(
                                Token(TokenType.SUB, "-", None, self.line)
                            )
                            self.state = 0
                        elif char == "*":
                            self.tokens.append(
                                Token(TokenType.MULT, "*", None, self.line)
                            )
                            self.state = 0
                        elif char == "!":
                            self.state = 8
                        elif char == '"':
                            current += char
                            self.state = 9
                        elif char == ";":
                            self.tokens.append(
                                Token(TokenType.SEMICOLON, ";", None, self.line)
                            )
                            self.state = 0
                        elif char == ",":
                            self.tokens.append(
                                Token(TokenType.COMMA, ",", None, self.line)
                            )
                            self.state = 0
                        else:
                            pass
                    case 1:
                        if char == "=":
                            self.tokens.append(
                                Token(TokenType.LESS_EQUAL, "<=", None, self.line)
                            )
                            self.state = 0  
                        else:
                            self.tokens.append(
                                Token(TokenType.LESS_THAN, "<", None, self.line)
                            )
                            self.state = 0
                    case 2:
                        if char == "=":
                            self.tokens.append(
                                Token(TokenType.EQUAL, "==", None, self.line)
                            )
                            self.state = 0
                        else:
                            self.tokens.append(
                                Token(TokenType.ASIGNATION, "=", None, self.line)
                            )
                            self.state = 0
                    case 3:
                        if char == "=":
                            self.tokens.append(
                                Token(TokenType.GREAT_EQUAL, ">=", None, self.line)
                            )
                            self.state = 0
                        else:
                            self.tokens.append(
                                Token(TokenType.GREAT, ">", None, self.line)
                            )
                            self.state = 0
                        pass
                    case 4:
                        if char.isdigit() or char == ".":
                            current += char
                        else:
                            self.tokens.append(
                                Token(TokenType.NUMBER, current, current, self.line)
                            )
                            current = ""
                            self.state = 0
                    case 5:
                        if char.isdigit() or char.isalpha():
                            current += char
                        else:
                            if current in self.reserved_words:
                                self.tokens.append(
                                    Token(
                                        self.reserved_words[current],
                                        current,
                                        None,
                                        self.line,
                                    )
                                )
                                current = ""
                                self.state = 0
                            else:
                                self.tokens.append(
                                    Token(
                                        TokenType.IDENTIFIER,
                                        current,
                                        None,
                                        self.line,
                                    )
                                )
                                current = ""
                                self.state = 0
                    case 6:
                        if char == "/":
                            self.state = 7
                        elif char == "*":
                            self.state = 11
                        else:
                            self.tokens.append(
                                Token(TokenType.DIAG, "/", None, self.line)
                            )
                            self.state = 0
                    case 7:
                        if char == "\n":
                            self.state = 0
                        else:
                            self.state = 7
                    case 8:
                        if char == "=":
                            self.tokens.append(
                                Token(TokenType.DIFERENT, "!=", None, self.line)
                            )
                            self.state = 0
                        else:
                            self.tokens.append(
                                Token(TokenType.NEGATION, "!", None, self.line)
                            )
                            self.state = 0
                    case 9:
                        if char == '"':
                            current += char
                            self.tokens.append(
                                Token(
                                    TokenType.IDENTIFIER,
                                    current,
                                    current[1:-1],
                                    self.line,
                                )
                            )
                            current = ""
                            self.state = 0
                        else:
                            current += char
                    case 11:
                        if char == "*":
                            self.state = 12
                    case 12:
                        if char == "/":
                            self.state = 0
                        else:
                            self.state = 11

            self.line += 1 

        self.tokens.append(
            Token(TokenType.EOF, None, None, self.line - 1)
        )  # Se termina el archivo y se agrega el token EOF
        return self.tokens  # Devuelve la lista de tokens generada

    def clean(
        self, cadena
    ):
        simbolos = [
            "(",
            ")",
            "{",
            "}",
            "=",
            "<",
            ">",
            "!",
            "+",
            "-",
            ";",
            "*",
            "/",
        ]
        clean_str = ""

        pattern = r"\/\/.*|\/\*[\s\S]*?\*\/|([A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?|\S)"
        result = re.findall(pattern, cadena)

        clean_str = " ".join(result)

        clean_str = clean_str.replace("/ *", "/*")
        clean_str = clean_str.replace("* /", "*/")
        clean_str = clean_str.replace("> =", ">=")
        clean_str = clean_str.replace("< =", "<=")
        clean_str = clean_str.replace("= =", "==")
        return f"{clean_str}\n"
