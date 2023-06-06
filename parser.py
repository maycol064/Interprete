from typing import List
from tokens import Token
from tokenType import TokenType

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.errors = False
        self.preanalysis = None
        self.i = 0

    def parse(self):
        self.preanalysis = self.tokens[self.i]
        self.PROGRAM()

        if not self.errors and not self.preanalysis.type == TokenType.EOF:
            Interprete.error(
                self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)
        elif not self.errors and self.preanalysis.type == TokenType.EOF:
            print("Consulta válida")
    
    def PROGRAM(self):
        if (self.preanalysis.type == TokenType.CLASS or self.preanalysis.type == TokenType.FUN or
            self.preanalysis.type == TokenType.VAR or self.preanalysis.type == TokenType.NEGATION or
            self.preanalysis.type == TokenType.LESS or self.preanalysis.type == TokenType.TRUE or
            self.preanalysis.type == TokenType.FALSE or self.preanalysis.type == TokenType.NULL or
            self.preanalysis.type == TokenType.THIS or self.preanalysis.type == TokenType.NUMBER or
            self.preanalysis.type == TokenType.STRING or self.preanalysis.type == TokenType.IDENTIFIER or
            self.preanalysis.type == TokenType.PARENT_OPEN or self.preanalysis.type == TokenType.SUPER or
            self.preanalysis.type == TokenType.FOR or self.preanalysis.type == TokenType.IF or
            self.preanalysis.type == TokenType.PRINT or self.preanalysis.type == TokenType.RETURN or
            self.preanalysis.type == TokenType.WHILE or self.preanalysis.type == TokenType.BRACKET_OPEN
        ):
            self.DECLARATION()
    
    def DECLARATION(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.CLASS:
            self.CLASS_DECL()
            self.DECLARATION()
        elif self.preanalysis.type == TokenType.FUN:
            self.FUN_DECL()
            self.DECLARATION()
        elif self.preanalysis.type == TokenType.VAR:
            self.VAR_DECL()
            self.DECLARATION()
        elif (
            self.preanalysis.type == TokenType.NEGATION or self.preanalysis.type == TokenType.LESS or
            self.preanalysis.type == TokenType.TRUE or self.preanalysis.type == TokenType.FALSE or
            self.preanalysis.type == TokenType.NULL or self.preanalysis.type == TokenType.THIS or
            self.preanalysis.type == TokenType.NUMBER or self.preanalysis.type == TokenType.STRING or
            self.preanalysis.type == TokenType.IDENTIFIER or self.preanalysis.type == TokenType.PARENT_OPEN or
            self.preanalysis.type == TokenType.SUPER or self.preanalysis.type == TokenType.FOR or
            self.preanalysis.type == TokenType.IF or self.preanalysis.type == TokenType.PRINT or
            self.preanalysis.type == TokenType.RETURN or self.preanalysis.type == TokenType.WHILE or
            self.preanalysis.type == TokenType.BRACKET_OPEN
        ):
            self.STATEMENT()
            self.DECLARATION()

    def CLASS_DECL(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.CLASS:
            self.matchToken(TokenType.CLASS)
            self.matchToken(TokenType.IDENTIFIER)
            self.CLASS_INHER()
            self.matchToken(TokenType.BRACKET_OPEN)
            self.FUNCTIONS()
            self.matchToken(TokenType.BRACKET_CLOSE)
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)
    
    def CLASS_INHER(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.LESS_THAN:
            self.matchToken(TokenType.LESS_THAN)
            self.matchToken(TokenType.IDENTIFIER)

    def FUN_DECL(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.FUN:
            self.matchToken(TokenType.FUN)
            self.FUNCTION()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def VAR_DECL(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.VAR:
            self.matchToken(TokenType.VAR)
            self.matchToken(TokenType.IDENTIFIER)
            self.VAR_INIT()
            self.matchToken(TokenType.SEMICOLON)
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def VAR_INIT(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.ASIGNATION:
            self.matchToken(TokenType.ASIGNATION)
            self.EXPRESSION()

    def STATEMENT(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.EXPR_STMT()
        elif self.preanalysis.type == TokenType.FOR:
            self.FOR_STMT()
        elif self.preanalysis.type == TokenType.IF:
            self.IF_STMT()
        elif self.preanalysis.type == TokenType.PRINT:
            self.PRINT_STMT()
        elif self.preanalysis.type == TokenType.RETURN:
            self.RETURN_STMT()
        elif self.preanalysis.type == TokenType.WHILE:
            self.WHILE_STMT()
        elif self.preanalysis.type == TokenType.BRACKET_OPEN:
            self.BLOCK()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)   

    def EXPR_STMT(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.EXPRESSION()
            self.matchToken(TokenType.SEMICOLON)
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def FOR_STMT(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.FOR:
            self.matchToken(TokenType.FOR)
            self.matchToken(TokenType.PARENT_OPEN)
            self.FOR_STMT_1()
            self.FOR_STMT_2()
            self.FOR_STMT_3()
            self.matchToken(TokenType.PARENT_CLOSE)
            self.STATEMENT()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def FOR_STMT_1(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.VAR:
            self.VAR_DECL()
        elif self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.EXPR_STMT()
        elif self.preanalysis.type == TokenType.SEMICOLON:
            self.matchToken(TokenType.SEMICOLON)
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def FOR_STMT_2(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.EXPRESSION()
            self.matchToken(TokenType.SEMICOLON)
        elif self.preanalysis.type == TokenType.SEMICOLON:
            self.matchToken(TokenType.SEMICOLON)
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)
    
    def FOR_STMT_3(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.EXPRESSION()

    def IF_STMT(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.IF:
            self.matchToken(TokenType.IF)
            self.matchToken(TokenType.PARENT_OPEN)
            self.EXPRESSION()
            self.matchToken(TokenType.PARENT_CLOSE)
            self.STATEMENT()
            self.ELSE_STATEMENT()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def ELSE_STATEMENT(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.ELSE:
            self.matchToken(TokenType.ELSE)
            self.STATEMENT()

    def PRINT_STMT(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.PRINT:
            self.matchToken(TokenType.PRINT)
            self.EXPRESSION()
            self.matchToken(TokenType.SEMICOLON)
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def RETURN_STMT(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.RETURN:
            self.matchToken(TokenType.RETURN)
            self.RETURN_EXP_OPC()
            self.matchToken(TokenType.SEMICOLON)
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def RETURN_EXP_OPC(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.EXPRESSION()

    def WHILE_STMT(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.WHILE:
            self.matchToken(TokenType.WHILE)
            self.matchToken(TokenType.PARENT_OPEN)
            self.EXPRESSION()
            self.matchToken(TokenType.PARENT_CLOSE)
            self.STATEMENT()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def BLOCK(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.BRACKET_OPEN:
            self.matchToken(TokenType.BRACKET_OPEN)
            self.BLOCK_DECL()
            self.matchToken(TokenType.BRACKET_CLOSE)
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def BLOCK_DECL(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.NEGATION,
                                TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER, TokenType.FOR, TokenType.IF,
                                TokenType.PRINT, TokenType.RETURN, TokenType.WHILE, TokenType.BRACKET_OPEN]:
            self.DECLARATION()
            self.BLOCK_DECL()

    def EXPRESSION(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.ASSIGNMENT()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def ASSIGNMENT(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.LOGIC_OR()
            self.ASSIGNMENT_OPC()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def ASSIGNMENT_OPC(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.ASIGNATION:
            self.matchToken(TokenType.ASIGNATION)
            self.EXPRESSION()

    def LOGIC_OR(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.LOGIC_AND()
            self.LOGIC_OR_2()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def LOGIC_OR_2(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.OR:
            self.matchToken(TokenType.OR)
            self.LOGIC_AND()
            self.LOGIC_OR_2()

    def LOGIC_AND(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.EQUALITY()
            self.LOGIC_AND_2()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def LOGIC_AND_2(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.AND:
            self.matchToken(TokenType.AND)
            self.EQUALITY()
            self.LOGIC_AND_2()

    def EQUALITY(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.COMPARISON()
            self.EQUALITY_2()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def EQUALITY_2(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.DIFERENT:
            self.matchToken(TokenType.DIFERENT)
            self.COMPARISON()
            self.EQUALITY_2()
        elif self.preanalysis.type == TokenType.EQUAL:
            self.matchToken(TokenType.EQUAL)
            self.COMPARISON()
            self.EQUALITY_2()

    def COMPARISON(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.TERM()
            self.COMPARISON_2()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def COMPARISON_2(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.GREAT_THAN:
            self.matchToken(TokenType.GREAT_THAN)
            self.TERM()
            self.COMPARISON_2()
        elif self.preanalysis.type == TokenType.GREAT_EQUAL:
            self.matchToken(TokenType.GREAT_EQUAL)
            self.TERM()
            self.COMPARISON_2()
        elif self.preanalysis.type == TokenType.LESS_THAN:
            self.matchToken(TokenType.LESS_THAN)
            self.TERM()
            self.COMPARISON_2()
        elif self.preanalysis.type == TokenType.LESS_EQUAL:
            self.matchToken(TokenType.LESS_EQUAL)
            self.TERM()
            self.COMPARISON_2()

    def TERM(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.FACTOR()
            self.TERM_2()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def TERM_2(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.LESS:
            self.matchToken(TokenType.LESS)
            self.FACTOR()
            self.TERM_2()
        elif self.preanalysis.type == TokenType.ADD:
            self.matchToken(TokenType.ADD)
            self.FACTOR()
            self.TERM_2()

    def FACTOR(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.UNARY()
            self.FACTOR_2()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def FACTOR_2(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.DIAG:
            self.matchToken(TokenType.DIAG)
            self.UNARY()
            self.FACTOR_2()
        elif self.preanalysis.type == TokenType.MULT:
            self.matchToken(TokenType.MULT)
            self.UNARY()
            self.FACTOR_2()

    def UNARY(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.NEGATION:
            self.matchToken(TokenType.NEGATION)
            self.UNARY()
        elif self.preanalysis.type == TokenType.LESS:
            self.matchToken(TokenType.LESS)
            self.UNARY()
        elif self.preanalysis.type in [TokenType.TRUE, TokenType.FALSE, TokenType.NULL, TokenType.THIS, TokenType.NUMBER,
                                TokenType.STRING, TokenType.IDENTIFIER, TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.CALL()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def CALL(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.TRUE, TokenType.FALSE, TokenType.NULL, TokenType.THIS, TokenType.NUMBER,
                                TokenType.STRING, TokenType.IDENTIFIER, TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.PRIMARY()
            self.CALL_2()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def CALL_2(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.PARENT_OPEN:
            self.matchToken(TokenType.PARENT_OPEN)
            self.ARGUMENTS_OPC()
            self.matchToken(TokenType.PARENT_CLOSE)
            self.CALL_2()
        elif self.preanalysis.type == TokenType.DOT:
            self.matchToken(TokenType.DOT)
            self.matchToken(TokenType.IDENTIFIER)
            self.CALL_2()
    
    def PRIMARY(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.TRUE:
            self.matchToken(TokenType.TRUE)
        elif self.preanalysis.type == TokenType.FALSE:
            self.matchToken(TokenType.FALSE)
        elif self.preanalysis.type == TokenType.NULL:
            self.matchToken(TokenType.NULL)
        elif self.preanalysis.type == TokenType.THIS:
            self.matchToken(TokenType.THIS)
        elif self.preanalysis.type == TokenType.NUMBER:
            self.matchToken(TokenType.NUMBER)
        elif self.preanalysis.type == TokenType.STRING:
            self.matchToken(TokenType.STRING)
        elif self.preanalysis.type == TokenType.IDENTIFIER:
            self.matchToken(TokenType.IDENTIFIER)
        elif self.preanalysis.type == TokenType.PARENT_OPEN:
            self.matchToken(TokenType.PARENT_OPEN)
            self.EXPRESSION()
            self.matchToken(TokenType.PARENT_CLOSE)
        elif self.preanalysis.type == TokenType.SUPER:
            self.matchToken(TokenType.SUPER)
            self.matchToken(TokenType.DOT)
            self.matchToken(TokenType.IDENTIFIER)
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def FUNCTION(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.IDENTIFIER:
            self.matchToken(TokenType.IDENTIFIER)
            self.matchToken(TokenType.PARENT_OPEN)
            self.PARAMETERS_OPC()
            self.matchToken(TokenType.PARENT_CLOSE)
            self.BLOCK()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def FUNCTIONS(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.IDENTIFIER:
            self.FUNCTION()
            self.FUNCTIONS()

    def PARAMETERS_OPC(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.IDENTIFIER:
            self.PARAMETERS()

    def PARAMETERS(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.IDENTIFIER:
            self.matchToken(TokenType.IDENTIFIER)
            self.PARAMETERS_2()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def PARAMETERS_2(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.COMMA:
            self.matchToken(TokenType.COMMA)
            self.matchToken(TokenType.IDENTIFIER)
            self.PARAMETERS_2()

    def ARGUMENTS_OPC(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.ARGUMENTS()

    def ARGUMENTS(self):
        if self.errors:
            return
        if self.preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            self.EXPRESSION()
            self.ARGUMENTS_2()
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "No se esperaba el token " + self.preanalysis.type)

    def ARGUMENTS_2(self):
        if self.errors:
            return
        if self.preanalysis.type == TokenType.COMMA:
            self.matchToken(TokenType.COMMA)
            self.EXPRESSION()
            self.ARGUMENTS_2()

    def matchToken(self, t):
        # global i, preanalysis, errors
        if self.errors:
            return
        if self.preanalysis.type == t:
            self.i += 1
            self.preanalysis = self.tokens[self.i]
        else:
            self.errors = True
            Interprete.error(self.preanalysis.line, "Se esperaba el token " + t)