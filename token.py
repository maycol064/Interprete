from typing import Optional


class Token:
    """A token in a programming language."""

    token_type: str
    lexeme: Optional[str]
    literal: Optional[object]
    line_number: int

    def __init__(self, token_type: str, lexeme: Optional[str] = None, literal: Optional[object] = None, line_number: int = 0):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line_number = line_number

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return False
        return self.token_type == other.token_type

    def __str__(self) -> str:
        return f"( {self.token_type} {self.lexeme} {self.literal} )"

