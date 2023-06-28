from tokens import Token
from tokenType import TokenType


class Postfixed:
    def __init__(self, tokens) -> None:
        self.infixed = tokens
        self.postfixed = []
        self.stack = []
        self.reserved_words = {
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

    def convert(self):
        controlStructure = False
        structureStack: list[Token] = []

        for index, t in enumerate(self.infixed):
            if t.type == TokenType.EOF:
                break

            if t.type in self.reserved_words.values():
                self.postfixed.append(t)
                if self.isControlStructure(t.type):
                    controlStructure = True
                    structureStack.append(t)
            elif self.isOperating(t.type):
                self.postfixed.append(t)
            elif t.type == TokenType.PARENT_OPEN:
                self.stack.append(t)
            elif t.type == TokenType.PARENT_CLOSE:
                while( ( len(self.stack) != 0) and (self.stack[-1].type != TokenType.PARENT_OPEN) ):
                    temp = self.stack.pop()
                    self.postfixed.append(temp)
                if self.stack[-1].type == TokenType.PARENT_OPEN:
                    self.stack.pop()
                if controlStructure:
                    self.postfixed.append(Token(TokenType.SEMICOLON,";",";",None))
            elif self.isOperator(t.type):
                while len(self.stack) != 0 and self.originGreatEqual(
                    self.stack[-1].type, t.type
                ):
                    temp = self.stack.pop()
                    self.postfixed.append(temp)
                self.stack.append(t)
            elif t.type == TokenType.SEMICOLON:
                while (
                    len(self.stack) != 0
                    and self.stack[-1].type != TokenType.BRACKET_OPEN
                ):
                    if controlStructure:
                        if structureStack[-1].type == TokenType.FOR: 
                            temp = self.stack.pop()
                            self.postfixed.append(temp)
                            break
                        pass
                    temp = self.stack.pop()
                    self.postfixed.append(temp)
                self.postfixed.append(t)
            elif t.type == TokenType.BRACKET_OPEN:
                self.stack.append(t)
            elif t.type == TokenType.BRACKET_CLOSE and controlStructure:
                if self.infixed[index + 1].type == TokenType.ELSE:
                    self.stack.pop()
                else:
                    self.stack.pop()
                    self.postfixed.append(Token(TokenType.SEMICOLON, ";", ";", None))
                    structureStack.pop()
                    if len(structureStack) == 0:
                        controlStructure = False

        while len(self.stack) != 0:
            temp = self.stack.pop()
            self.postfixed.append(temp)

        while len(structureStack) != 0:
            structureStack.pop()
            self.postfixed.append(Token(TokenType.SEMICOLON, ";", ";", None))

        return self.postfixed

    def isOperating(self, type) -> bool:
        match type:
            case TokenType.IDENTIFIER:
                return True
            case TokenType.NUMBER | TokenType.STRING | TokenType.TRUE | TokenType.FALSE:
                return True
            case other:
                return False

    def isOperator(self, type) -> bool:
        match type:
            case TokenType.ADD | TokenType.SUB | TokenType.MULT | TokenType.DIAG:
                return True
            case TokenType.EQUAL | TokenType.DIFERENT | TokenType.GREAT | TokenType.GREAT_EQUAL:
                return True
            case TokenType.AND | TokenType.OR | TokenType.ASIGNATION:
                return True
            case TokenType.LESS_THAN | TokenType.LESS_EQUAL:
                return True
            case other:
                return False

    def isControlStructure(self, type) -> bool:
        match type:
            case TokenType.IF | TokenType.ELSE:
                return True
            case TokenType.WHILE | TokenType.FOR:
                return True
            case _:
                return False

    def originGreatEqual(self, type1, type2) -> bool:
        return self.getOrigin(type1) >= self.getOrigin(type2)

    def getOrigin(self, type) -> bool:
        match type:
            case TokenType.MULT | TokenType.DIAG:
                return 7
            case TokenType.ADD | TokenType.SUB:
                return 6
            case TokenType.GREAT_EQUAL | TokenType.GREAT | TokenType.LESS_THAN | TokenType.LESS_EQUAL:
                return 5
            case TokenType.DIFERENT | TokenType.EQUAL:
                return 4
            case TokenType.AND:
                return 3
            case TokenType.OR:
                return 2
            case TokenType.ASIGNATION:
                return 1
            case _:
                return 0

    def aridad(self, type: TokenType):
        match type:
            case TokenType.MULT| TokenType.DIAG| TokenType.SUB| TokenType.ADD| TokenType.EQUAL| TokenType.GREAT| TokenType.GREAT_EQUAL | TokenType.ASIGNATION:
                return 2
            case TokenType.LESS_THAN | TokenType.LESS_EQUAL | TokenType.DIFERENT | TokenType.AND | TokenType.OR :
                return 2
            case other:
                return 0
