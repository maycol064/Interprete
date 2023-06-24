from typing import Optional
from tokenType import TokenType


class Token:
    """A token in a programming language."""

    type: str
    lexeme: Optional[str]
    literal: Optional[object]
    line: int

    def __init__(self, type: str, lexeme: Optional[str] = None, literal: Optional[object] = None, line: int = 0):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return False
        return self.type == other.type

    def __str__(self) -> str:
        return f"--> {self.type} | lex: {self.lexeme} | lit: {self.literal} | line: {self.line}"

    # Auxiliars methods
    def isOperating(self) -> bool:
        match self.type:
            case TokenType.IDENTIFIER, TokenType.NUMBER:
                return True
                pass
            case other:
                return False
                pass
