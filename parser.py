from typing import List
from token import Token
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

        if not self.errors and not self.preanalysis.token_type.equals(TokenType.EOF):
            Interprete.error(
                self.preanalysis.linea, "No se esperaba el token " + self.preanalysis.type)
        elif not self.errors and self.preanalysis.type.equals(TokenType.EOF):
            print("Consulta válida")
    
    def PROGRAM(self):
        if (preanalysis.type == TokenType.CLASS or preanalysis.type == TokenType.FUN or
            preanalysis.type == TokenType.VAR or preanalysis.type == TokenType.NEGATION or
            preanalysis.type == TokenType.LESS or preanalysis.type == TokenType.TRUE or
            preanalysis.type == TokenType.FALSE or preanalysis.type == TokenType.NULL or
            preanalysis.type == TokenType.THIS or preanalysis.type == TokenType.NUMBER or
            preanalysis.type == TokenType.STRING or preanalysis.type == TokenType.IDENTIFIER or
            preanalysis.type == TokenType.PARENT_OPEN or preanalysis.type == TokenType.SUPER or
            preanalysis.type == TokenType.FOR or preanalysis.type == TokenType.IF or
            preanalysis.type == TokenType.PRINT or preanalysis.type == TokenType.RETURN or
            preanalysis.type == TokenType.WHILE or preanalysis.type == TokenType.BRACKET_OPEN
        ):
            DECLARATION()
    
    def DECLARATION(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.CLASS:
            CLASS_DECL()
            DECLARATION()
        elif preanalysis.type == TokenType.FUN:
            FUN_DECL()
            DECLARATION()
        elif preanalysis.type == TokenType.VAR:
            VAR_DECL()
            DECLARATION()
        elif (
            preanalysis.type == TokenType.NEGATION or preanalysis.type == TokenType.LESS or
            preanalysis.type == TokenType.TRUE or preanalysis.type == TokenType.FALSE or
            preanalysis.type == TokenType.NULL or preanalysis.type == TokenType.THIS or
            preanalysis.type == TokenType.NUMBER or preanalysis.type == TokenType.STRING or
            preanalysis.type == TokenType.IDENTIFIER or preanalysis.type == TokenType.PARENT_OPEN or
            preanalysis.type == TokenType.SUPER or preanalysis.type == TokenType.FOR or
            preanalysis.type == TokenType.IF or preanalysis.type == TokenType.PRINT or
            preanalysis.type == TokenType.RETURN or preanalysis.type == TokenType.WHILE or
            preanalysis.type == TokenType.BRACKET_OPEN
        ):
            STATEMENT()
            DECLARATION()

    def CLASS_DECL(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.CLASS:
            matchToken(TokenType.CLASS)
            matchToken(TokenType.IDENTIFIER)
            CLASS_INHER()
            matchToken(TokenType.BRACKET_OPEN)
            FUNCTIONS()
            matchToken(TokenType.BRACKET_CLOSE)
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)
    
    def CLASS_INHER(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.LESS_THAN:
            matchToken(TokenType.LESS_THAN)
            matchToken(TokenType.IDENTIFIER)

    def FUN_DECL(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.FUN:
            matchToken(TokenType.FUN)
            FUNCTION()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def VAR_DECL(self):
        if self.erros:
            return
        if preanalysis.type == TokenType.VAR:
            matchToken(TokenType.VAR)
            matchToken(TokenType.IDENTIFIER)
            VAR_INIT()
            matchToken(TokenType.SEMICOLON)
        else:
            self.erros = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def VAR_INIT(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.ASIGNATION:
            matchToken(TokenType.ASIGNATION)
            EXPRESSION()

    def STATEMENT(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            EXPR_STMT()
        elif preanalysis.type == TokenType.FOR:
            FOR_STMT()
        elif preanalysis.type == TokenType.IF:
            IF_STMT()
        elif preanalysis.type == TokenType.PRINT:
            PRINT_STMT()
        elif preanalysis.type == TokenType.RETURN:
            RETURN_STMT()
        elif preanalysis.type == TokenType.WHILE:
            WHILE_STMT()
        elif preanalysis.type == TokenType.BRACKET_OPEN:
            BLOCK()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)   

    def EXPR_STMT(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            EXPRESSION()
            matchToken(TokenType.SEMICOLON)
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def FOR_STMT(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.FOR:
            matchToken(TokenType.FOR)
            matchToken(TokenType.PARENT_OPEN)
            FOR_STMT_1()
            FOR_STMT_2()
            FOR_STMT_3()
            matchToken(TokenType.PARENT_CLOSE)
            STATEMENT()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def FOR_STMT_1(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.VAR:
            VAR_DECL()
        elif preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            EXPR_STMT()
        elif preanalysis.type == TokenType.SEMICOLON:
            matchToken(TokenType.SEMICOLON)
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def FOR_STMT_2(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            EXPRESSION()
            matchToken(TokenType.SEMICOLON)
        elif preanalysis.type == TokenType.SEMICOLON:
            matchToken(TokenType.SEMICOLON)
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)
    
    def FOR_STMT_3(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            EXPRESSION()

    def IF_STMT(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.IF:
            matchToken(TokenType.IF)
            matchToken(TokenType.PARENT_OPEN)
            EXPRESSION()
            matchToken(TokenType.PPARENT_CLOSE)
            STATEMENT()
            ELSE_STATEMENT()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def ELSE_STATEMENT(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.ELSE:
            matchToken(TokenType.ELSE)
            STATEMENT()

    def PRINT_STMT(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.PRINT:
            matchToken(TokenType.PRINT)
            EXPRESSION()
            matchToken(TokenType.SEMICOLON)
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def RETURN_STMT(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.RETURN:
            matchToken(TokenType.RETURN)
            RETURN_EXP_OPC()
            matchToken(TokenType.SEMICOLON)
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def RETURN_EXP_OPC(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            EXPRESSION()

    def WHILE_STMT(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.WHILE:
            matchToken(TokenType.WHILE)
            matchToken(TokenType.PARENT_OPEN)
            EXPRESSION()
            matchToken(TokenType.PARENT_CLOSE)
            STATEMENT()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def BLOCK(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.BRACKET_OPEN:
            matchToken(TokenType.BRACKET_OPEN)
            BLOCK_DECL()
            matchToken(TokenType.BRACKET_CLOSE)
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def BLOCK_DECL(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.NEGATION,
                                TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER, TokenType.FOR, TokenType.IF,
                                TokenType.PRINT, TokenType.RETURN, TokenType.WHILE, TokenType.BRACKET_OPEN]:
            DECLARATION()
            BLOCK_DECL()

    def EXPRESSION(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            ASSIGNMENT()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def ASSIGNMENT(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            LOGIC_OR()
            ASSIGNMENT_OPC()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def ASSIGNMENT_OPC(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.ASIG:
            matchToken(TokenType.ASIG)
            EXPRESSION()

    def LOGIC_OR(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            LOGIC_AND()
            LOGIC_OR_2()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def LOGIC_OR_2(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.OR:
            matchToken(TokenType.OR)
            LOGIC_AND()
            LOGIC_OR_2()

    def LOGIC_AND(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            EQUALITY()
            LOGIC_AND_2()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def LOGIC_AND_2(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.AND:
            matchToken(TokenType.AND)
            EQUALITY()
            LOGIC_AND_2()

    def EQUALITY(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            COMPARISON()
            EQUALITY_2()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def EQUALITY_2(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.DIFERENT:
            matchToken(TokenType.DIFERENT)
            COMPARISON()
            EQUALITY_2()
        elif preanalysis.type == TokenType.EQUAL:
            matchToken(TokenType.EQUAL)
            COMPARISON()
            EQUALITY_2()

    def COMPARISON(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            TERM()
            COMPARISON_2()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def COMPARISON_2(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.GREAT_THAN:
            matchToken(TokenType.GREAT_THAN)
            TERM()
            COMPARISON_2()
        elif preanalysis.type == TokenType.GREAT_EQUAL:
            matchToken(TokenType.GREAT_EQUAL)
            TERM()
            COMPARISON_2()
        elif preanalysis.type == TokenType.LESS_THAN:
            matchToken(TokenType.LESS_THAN)
            TERM()
            COMPARISON_2()
        elif preanalysis.type == TokenType.LESS_EQUAL:
            matchToken(TokenType.LESS_EQUAL)
            TERM()
            COMPARISON_2()

    def TERM(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            FACTOR()
            TERM_2()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def TERM_2(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.LESS:
            matchToken(TokenType.LESS)
            FACTOR()
            TERM_2()
        elif preanalysis.type == TokenType.MAS:
            matchToken(TokenType.MAS)
            FACTOR()
            TERM_2()

    def FACTOR(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            UNARY()
            FACTOR_2()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def FACTOR_2(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.DIAG:
            matchToken(TokenType.DIAG)
            UNARY()
            FACTOR_2()
        elif preanalysis.type == TokenType.MULT:
            matchToken(TokenType.MULT)
            UNARY()
            FACTOR_2()

    def UNARY(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.NEGATION:
            matchToken(TokenType.NEGATION)
            UNARY()
        elif preanalysis.type == TokenType.LESS:
            matchToken(TokenType.LESS)
            UNARY()
        elif preanalysis.type in [TokenType.TRUE, TokenType.FALSE, TokenType.NULL, TokenType.THIS, TokenType.NUMBER,
                                TokenType.STRING, TokenType.IDENTIFIER, TokenType.PARENT_OPEN, TokenType.SUPER]:
            CALL()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def CALL(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.TRUE, TokenType.FALSE, TokenType.NULL, TokenType.THIS, TokenType.NUMBER,
                                TokenType.STRING, TokenType.IDENTIFIER, TokenType.PARENT_OPEN, TokenType.SUPER]:
            PRIMARY()
            CALL_2()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def CALL_2(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.PARENT_OPEN:
            matchToken(TokenType.PARENT_OPEN)
            ARGUMENTS_OPC()
            matchToken(TokenType.PARENT_CLOSE)
            CALL_2()
        elif preanalysis.type == TokenType.DOT:
            matchToken(TokenType.DOT)
            matchToken(TokenType.IDENTIFIER)
            CALL_2()
    
    def PRIMARY(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.TRUE:
            matchToken(TokenType.TRUE)
        elif preanalysis.type == TokenType.FALSE:
            matchToken(TokenType.FALSE)
        elif preanalysis.type == TokenType.NULL:
            matchToken(TokenType.NULL)
        elif preanalysis.type == TokenType.THIS:
            matchToken(TokenType.THIS)
        elif preanalysis.type == TokenType.NUMBER:
            matchToken(TokenType.NUMBER)
        elif preanalysis.type == TokenType.STRING:
            matchToken(TokenType.STRING)
        elif preanalysis.type == TokenType.IDENTIFIER:
            matchToken(TokenType.IDENTIFIER)
        elif preanalysis.type == TokenType.PARENT_OPEN:
            matchToken(TokenType.PARENT_OPEN)
            EXPRESSION()
            matchToken(TokenType.PARENT_CLOSE)
        elif preanalysis.type == TokenType.SUPER:
            matchToken(TokenType.SUPER)
            matchToken(TokenType.DOT)
            matchToken(TokenType.IDENTIFIER)
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def FUNCTION(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.IDENTIFIER:
            matchToken(TokenType.IDENTIFIER)
            matchToken(TokenType.PARENT_OPEN)
            PARAMETERS_OPC()
            matchToken(TokenType.PARENT_CLOSE)
            BLOCK()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def FUNCTIONS(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.IDENTIFIER:
            FUNCTION()
            FUNCTIONS()

    def PARAMETERS_OPC(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.IDENTIFIER:
            PARAMETERS()

    def PARAMETERS(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.IDENTIFIER:
            matchToken(TokenType.IDENTIFIER)
            PARAMETERS_2()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def PARAMETERS_2(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.COMMA:
            matchToken(TokenType.COMMA)
            matchToken(TokenType.IDENTIFIER)
            PARAMETERS_2()

    def ARGUMENTS_OPC(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            ARGUMENTS()

    def ARGUMENTS(self):
        if self.errors:
            return
        if preanalysis.type in [TokenType.NEGATION, TokenType.LESS, TokenType.TRUE, TokenType.FALSE, TokenType.NULL,
                                TokenType.THIS, TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER,
                                TokenType.PARENT_OPEN, TokenType.SUPER]:
            EXPRESSION()
            ARGUMENTS_2()
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "No se esperaba el token " + preanalysis.type)

    def ARGUMENTS_2(self):
        if self.errors:
            return
        if preanalysis.type == TokenType.COMMA:
            matchToken(TokenType.COMMA)
            EXPRESSION()
            ARGUMENTS_2()

    def matchToken(t):
        global i, preanalisis, errors
        if self.errors:
            return
        if preanalysis.type == t:
            i += 1
            preanalisis = tokens[i]
        else:
            self.errors = True
            Interprete.error(preanalysis.line, "Se esperaba el token " + t)