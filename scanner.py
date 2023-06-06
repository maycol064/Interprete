from tokenType import TokenType
from tokens import Token
import string

class Scanner:
    def __init__(self, source) -> None:
        self.source = source
        self.line = 0
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
            'while' : TokenType.WHILE,
        }

    def scanTokens(self) -> list[TokenType]:
        state = 0
        aux=0
        while self.line<len(self.source):
            current = ''
            while 1:
                lineux = (self.source[self.line])
                lineux += ' '                
                char=lineux[aux]
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
                            self.tokens.append(Token(TokenType.BRACKET_OPEN, '{', None, self.line))
                            state = 0
                        elif char == '}':
                            self.tokens.append(Token(TokenType.BRACKET_CLOSE, '}', None, self.line))
                            state = 0
                        elif char == '(':
                            self.tokens.append(Token(TokenType.PARENT_OPEN, '(', None, self.line))
                            state = 0
                        elif char == ')':
                            self.tokens.append(Token(TokenType.PARENT_CLOSE, ')', None, [self.line]))
                            state = 0
                        elif char == '+':
                            self.tokens.append(Token(TokenType.ADD, '+', None,[self.line]))
                            state = 0
                        elif char == '-':
                            self.tokens.append(Token(TokenType.SUB, '-', None,[self.line]))
                            state = 0
                        elif char == '*':
                            self.tokens.append(Token(TokenType.MULT, '*', None, [self.line]))
                            state = 0
                        elif char == '!':
                            state = 8
                        elif char == '"':
                            current += char
                            state = 9
                        elif char == ';':
                            self.tokens.append(Token(TokenType.SEMICOLON, ';', None,[self.line]))
                            state = 0
                        elif char == ',':
                            self.tokens.append(Token(TokenType.COMMA, ',', None, [self.line]))
                            state = 0
                        elif char==".":
                            self.tokens.append(Token(TokenType.DOT, '.', None, [self.line]))
                            state = 0
                        else:
                            pass
                        aux+=1
                    case 1:        
                        if char == '=':
                            self.tokens.append(Token(TokenType.LESSEQUAL, '<=', None,[self.line]))
                            state = 0
                            aux+=1
                        else:
                            self.tokens.append(Token(TokenType.LESS, '<', None, [self.line]))
                            state = 0
                    case 2:
                        if char == '=':
                            self.tokens.append(Token(TokenType.EQUAL, '==', None,[self.line]))
                            state = 0
                            aux+=1
                        else:
                            self.tokens.append(Token(TokenType.ASIGNATION, '=', None, [self.line]))
                            state = 0
                    case 3:
                        if char == '=':
                            self.tokens.append(Token(TokenType.GREATEQUAL, '>=', None, [self.line]))
                            state = 0
                        else:
                            self.tokens.append(Token(TokenType.GREAT, '>', None, [self.line]))
                            state=0
                            aux+=1
                        pass
                    case 4:
                        if char.isdigit():
                            current += char
                            aux+=1
                        elif char == ".":
                            current += char
                            aux+=1
                            state=13
                        else:
                            self.tokens.append(Token(TokenType.NUMBER, current, current, [self.line]))
                            current = ''
                            state = 0
                    case 5:
                        if char.isdigit() or char.isalpha():
                            current += char
                            aux+=1
                        else:
                            if current in self.reservedWords:
                                self.tokens.append(Token(self.reservedWords[current], current, None, [self.line]))
                                current = ''
                                state = 0
                            else:
                                self.tokens.append(Token(TokenType.IDENTIFIER, current, None, [self.line]))
                                current = ''
                                state = 0
                    case 6:
                        if char == '/':
                            state = 7
                        elif char == '*':
                            state = 11
                        else:
                            self.tokens.append(Token(TokenType.DIVID, '/', None, [self.line]))
                            state = 0
                    case 7:
                        if char=='/':
                            self.tokens.append(Token(TokenType.COMMENT, "//", self.source[self.line], [self.line]))
                            if self.line+1==len(self.source):
                                self.source.pop()
                                break

                            else:
                                self.line +=1
                            aux=0
                            state= 0
                    case 8:
                        if char == "=":
                            aux+=1
                            self.tokens.append(Token(TokenType.DIFFERENT, "!=", None, [self.line]))
                            state = 0
                        else:
                            self.tokens.append(Token(TokenType.NEGATION, "!", None, [self.line]))
                            state = 0
                    case 9:
                        aux+=1
                        if char == '"':
                            current += char
                            self.tokens.append(Token(TokenType.MULTCOMMENT, "\"\"", current[1:-1], [self.line]))
                            current = ""
                            state = 0
                        else:
                            current += char
                    case 10:
                        # Aquí van los comentarios, no le supimos ajajaja+
                        print()
                    case 11:
                        aux+=1
                        current+=char
                        if char == "*":
                            state = 12
                    case 12:
                        if char == "/":
                            self.tokens.append(Token(TokenType.MULTCOMMENT, "/* */", current[1:-1], [self.line]))
                            aux+=1
                            current=''
                            state = 0                            
                        else:
                            state = 11
                    case 13:
                        if char.isdigit():
                            current += char
                            aux+=1
                        else:
                            self.tokens.append(Token(TokenType.NUMBER, current, current, [self.line]))
                            current = ''
                            state = 0
    
                if(aux==len(lineux)):
                    self.line+=1
                    self.source.pop()
                    aux=0
                    break
            
        self.tokens.append(Token(TokenType.EOF, None, None, self.line-1))

        return self.tokens

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