from tokenType import TokenType

class Token:
    def __init__(self, type: TokenType, lexeme: str, literal, line: int) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal ##Palabra reservada no lleva literal
        self.line = line
    
    def __repr__(self) -> str:
        return f"--> {self.type} | lex: {self.lexeme} | lit: {self.literal} | line: #{self.line}"