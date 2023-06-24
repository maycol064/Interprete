from tokens import Token
from tokenType import TokenType


class Postfixed:
    def __init__(self, tokens) -> None:
        self.infixed = tokens
        self.postfixed = []
        self.stack = []
        self.reserved_words = {  
            "and": TipoToken.AND,
            "class": TipoToken.CLASS,
            "also": TipoToken.ALSO,
            "for": TipoToken.FOR,
            "fun": TipoToken.FUN,
            "if": TipoToken.IF,
            "null": TipoToken.NULL,
            "print": TipoToken.PRINT,
            "return": TipoToken.RETURN,
            "super": TipoToken.SUPER,
            "this": TipoToken.THIS,
            "true": TipoToken.TRUE,
            "var": TipoToken.VAR,
            "while": TipoToken.WHILE,
            "else": TipoToken.ELSE
        }

    def convert(self):
        controlStructure = False
        stackStructure = []
        for index, token in enumerate(self.infixed):
            if token.type == TokenType.EOF:
                break
            if token.type in self.reserved_words.values():
                self.postfixed.append(token)
                if self.isControlStructure(token.type):
                    controlStructure = True
                    stackStructure.append(token)
            elif self.isOperator(token.type):
                self.postfixed.append(token)
            elif token.type == TokenType.PARENT_OPEN:
                self.stack.append(token)
            elif token.type == TokenType.PARENT_CLOSE:
                while len(self.stack) != 0 and self.stack[-1].type != TokenType.PARENT_CLOSE:
                    temp = self.stack.pop()
                    self.postfixed.append(temp)
                if self.stack[-1].type == TokenType.PARENT_OPEN:
                    self.stack.pop()
                if controlStructure:
                    self.postfixed.append(Token(TokenType.SEMICOLON, ';', ';', None))
            elif self.isOperator(token.type):
                while len(self.stack) != 0 and self.originGreatEqual(self.stack[-1].type, token.type):
                    temp = self.stack.pop()
                    self.postfixed.append(temp)
                self.stack.append(token)
            elif token.type == TokenType.SEMICOLON:
                while len(self.stack) != 0 and self.stack[-1].type != TokenType.BRACKET_OPEN:
                    temp = self.stack.pop()
                    self.postfixed.append(temp)
                self.postfixed.append(token)
            elif token.type == TokenType.BRACKET_OPEN:
                self.stack.append(token)
            elif token.type == TokenType.BRACKET_CLOSE and controlStructure:
                if self.infixed[index + 1].type == TokenType.ELSE:
                    self.stack.pop()
                else:
                    self.stack.pop()
                    self.postfixed.append(Token(TokenType.SEMICOLON, ';', ';', None))
                    stackStructure.pop()
                    if len(stackStructure) == 0:
                        controlStructure = False
        while(len(self.stack) != 0):
            temp = self.stack.pop()
            self.postfixed.append(temp)
        while(len(stackStructure) != 0):
            stackStructure.pop()
            self.postfixed.append(Token(TokenType.SEMICOLON, ';', ';', None))
        
        return self.postfixed
    
    def isControlStructure(self, type):
        return type in [TokenType.IF, TokenType.ELSE, TokenType.WHILE]

    def isOperator(self, type):
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
    
    def originGreatEqual(self, type1, type2):
        return self.getOrigin(type1) >= self.getOrigin(type2)

    def getOrigin(self, type):
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
        