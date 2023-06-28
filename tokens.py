from typing import Optional
from tokenType import TokenType


class Token:
    def __init__(self, type: TokenType, lexeme: str = None, literal: Optional[object] = None, line: int = 0):
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
    def isOperating(self, type) -> bool:
        return type in [
            TokenType.IDENTIFIER,
            TokenType.NUMBER
        ]
    
    def isOperator(self, type) -> bool:
        return type in [
            TokenType.ADD, 
            TokenType.SUB, 
            TokenType.MULT, 
            TokenType.DIAG,
            TokenType.EQUAL,
            TokenType.GREAT,
            TokenType.GREAT_THAN,
            TokenType.GREAT_EQUAL,
            TokenType.LESS,
            TokenType.LESS_THAN,
            TokenType.LESS_EQUAL,
            TokenType.ASIGNATION,
        ]

    def isRevervedWord(self, type) -> bool:
        return type in [
            TokenType.VAR, 
            TokenType.IF, 
            TokenType.PRINT, 
            TokenType.ELSE
        ]

    def isControlStructure(self, type) -> bool:
        return type in [
            TokenType.IF, 
            TokenType.ELSE, 
            TokenType.WHILE
        ]
    
    def originGreatEqual(self, type1, type2) -> bool:
        return self.getOrigin(type1) >= self.getOrigin(type2)

    def getOrigin(self, type) -> bool:
        if type in [TokenType.MULT, TokenType.DIAG]:
            return 3
        if type in [TokenType.ADD, TokenType.SUB]:
            return 2
        if type in [
            TokenType.EQUAL,
            TokenType.GREAT,
            TokenType.GREAT_THAN,
            TokenType.GREAT_EQUAL,
            TokenType.LESS,
            TokenType.LESS_THAN,
            TokenType.LESS_EQUAL,
            TokenType.ASIGNATION,
        ]:
            return 1
        return 0
    
    def aridad(self, type):
        if type in [
            TokenType.MULT,
            TokenType.DIAG,
            TokenType.ADD,
            TokenType.SUB,
            TokenType.EQUAL,
            TokenType.GREAT,
            TokenType.GREAT_EQUAL
        ]: 
            return 2
        return 0
