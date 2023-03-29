from tokenType import TokenType
from token import Token
import string

class Scanner:
    def __init__(self, source) -> None:
        self.source = source
        self.line = 1
        self.tokens = []
        self.reservedWords = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'also': TokenType.ALSO,
            'for': TokenType.FOR,
            'fun' : TokenType.FUN,
            'if' : TokenType.IF,
            'null' : TokenType.NULL,
            'print' : TokenType.PRINT,
            'return' : TokenType.RETURN,
            'super' : TokenType.SUPER,
            'this' : TokenType.THIS,
            'true' : TokenType.TRUE,
            'var' : TokenType.VAR,
            'while' : TokenType.WHILE
        }

    def tokensScan(self) -> list[TokenType]:
        state = 0
        for line in self.source:
            current = ''
            lineux = self.cleanLine(line)
            lineux += ' '

            for char in lineux:
                match state:
                    case 0:
                        if char == '<':
                            state = 1  
                        elif char == '=':
                            state = 2
                        elif char == '>':
                            state = 3
                        elif char.isdigit():
                           current += char
                           state = 4
                        elif char.isalpha():
                            current += char
                            state = 5
                        elif char == '/':
                            state = 6
                        elif char == '{':
                            self.tokens.append(Token(TokenType.OPENBRACKET, '{', None, self.line))
                            state = 0
                        elif char == '}':
                            self.tokens.append(Token(TokenType.CLOSEBRACKET, '}', None, self.line))
                            state = 0
                        elif char == '(':
                            self.tokens.append(Token(TokenType.OPENPARENT, '(', None, self.line))
                            state = 0
                        elif char == ')':
                            self.tokens.append(Token(TokenType.CLOSEPARENT, ')', None, self.line))
                            state = 0
                        elif char == '+':
                            self.tokens.append(Token(TokenType.ADD, '+', None, self.line))
                            state = 0
                        elif char == '-':
                            self.tokens.append(Token(TokenType.SUB, '-', None, self.line))
                            state = 0
                        elif char == '*':
                            self.tokens.append(Token(TokenType.MULT, '*', None, self.line))
                            state = 0
                        elif char == '!':
                            state = 8
                        elif char == '"':
                            current += char
                            state = 9
                        elif char == ';':
                            self.tokens.append(Token(TokenType.DOTCOMMA, ';', None, self.line))
                            state = 0
                        elif char == ',':
                            self.tokens.append(Token(TokenType.COMMA, ',', None, self.line))
                            state = 0 
                        else:
                            pass
                    case 1:        
                        if char == '=':
                            self.tokens.append(Token(TokenType.LESSEQUAL, '<=', None, self.line))
                            state = 0
                        else:
                            self.tokens.append(Token(TokenType.LESS, '<', None, self.line))
                            state = 0
                    case 2:
                        if char == '=':
                            self.tokens.append(Token(TokenType.EQUAL, '==', None, self.line))
                            state = 0
                        else:
                            self.tokens.append(Token(TokenType.ASIGNATION, '=', None, self.line))
                            state = 0
                    case 3:
                        if char == '=':
                            self.tokens.append(Token(TokenType.GREATEQUAL, '>=', None, self.line))
                            state = 0
                        else:
                            self.tokens.append(Token(TokenType.GREAT, '>', None, self.line))
                            state=0
                        pass
                    case 4:
                        if char.isdigit() or char == '.':
                            current += char
                        else:
                            self.tokens.append(Token(TokenType.NUMBER, current, current, self.line))
                            current = ''
                            state = 0
                    case 5:
                        if char.isdigit() or char.isalpha():
                            current += char
                        else:
                            if current in self.reservedWords:
                                self.tokens.append(Token(self.reservedWords[current], current, None, self.line))
                                current = ''
                                state = 0
                            else:
                                self.tokens.append(Token(TokenType.IDENTIFIER, current, None, self.line))
                                current = ''
                                state = 0
                    case 6:
                        if char == '/':
                            state = 7
                        elif char == '*':
                            state = 11
                        else:
                            self.tokens.append(Token(TokenType.DIVID, '/', None, self.line))
                            state = 0
                    case 7:
                        if char == '\n':
                            state = 0
                        else:
                            state = 7
                    case 8:
                        if char == "=":
                            self.tokens.append(Token(TokenType.DIFFERENT, "!=", None, fself.line))
                            state = 0
                        else:
                            self.tokens.append(Token(TokenType.NEGATION, "!", None, self.line))
                            state = 0
                    case 9:
                        if char == '"':
                            current += char
                            self.tokens.append(Token(TokenType.IDENTIFIER, current, current[1:-1], self.line))
                            current = ""
                            state = 0
                        else:
                            current += char
                    case 11:
                        if char == "*":
                            state = 12
                    case 12:
                        if char == "/":
                            state = 0
                        else:
                            state = 11

    def cleanLine(self, string):
        symbols = ['(', ')' ,'{' ,'}', '=', '<', '>', '!', '+', '-', ';', '*', '/']
        cleanString = ''
        current = ''
        control = True
        state = 0
        char = 0
        string = string.replace(" ","")
        while control:
            match state:
                case 0:
                    try:
                        if string[char] in symbols:
                            current = string[char]
                            state = 1
                        elif string[char].isdigit():
                            current = string[char]
                            state = 2
                        elif string[char].isalpha():
                            current += string[char]
                            state = 3
                        elif string[char] == '"':
                            current += string[char]
                            state = 4
                        else:
                            control = False
                    except:
                        control = False
                case 1:
                    try:
                        if string[char+1] in symbols:
                            current += string[char+1]
                            char +=1
                            state = 1
                        else:
                            cleanString += f" {current}"
                            current = ""
                            char += 1
                            state = 0
                    except:
                        cleanString += f" {current} "
                        current = ""
                        char += 1
                        state = 0
                        control = False

                case 2:
                    try:
                        if string[char+1].isdigit() or string[char+1] == ".":
                            current += string[char+1]
                            char +=1
                        elif string[char+1] == ",":
                            cleanString += f" {current} ,"
                            char += 2
                            current = ""
                            state = 0
                        else:
                            cleanString += f" {current}"
                            current = ""
                            char += 1
                            state = 0
                    except:
                        cleanString += f" {current}"
                        current = ""
                        char += 1
                        state = 0
                        control = False
                case 3:
                    try:
                        if string[char+1].isalpha() or string[char+1].isdigit():
                            current += string[char+1]
                            char += 1
                        elif string[char+1] == ",":
                            cleanString += f" {current} ,"
                            char += 2
                            current = ""
                            state = 0
                        else:
                            cleanString += f" {current} "
                            current = ""
                            char += 1
                            state = 0
                    except:
                        control = False
                case 4:
                    try:
                        if string[char+1] != '"':
                            current += string[char+1]
                            char +=1
                        else:
                            cleanString += f' {current}" '
                            current = ""
                            char +=1
                            state = 0
                    except:
                        control = False
            
        return f"{cleanString}\n"