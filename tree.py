from tokenType import TokenType
from tokens import Token
from node import Node
from postfixedGenerator import Postfixed
from symbolsTable import SymbolsTable
from solverRelational import SolverRelational
from solverArithmetic import SolverArithmetic
from solverLogic import SolverLogic
import sys


class Tree:
    def __init__(self, root: Node) -> None:
        self.root = root
        self.posthelp = Postfixed(None)
        self.tsym = SymbolsTable()

    def iterate(self):
        for index, n in enumerate(self.root.children):
            t = n.value
            match t.type:
                case TokenType.ADD | TokenType.SUB | TokenType.MULT | TokenType.DIAG:
                    solver = SolverArithmetic()
                    res = solver.resolver(n)
                    print(f"{res}")
                case TokenType.VAR:
                    self.solverVar(n)
                case TokenType.IF:
                    self.resolverIf(n)
                case TokenType.WHILE:
                    self.solverWhile(n)
                case TokenType.FOR:
                    self.solverFor(n)
                    pass
                case TokenType.GREAT_EQUAL | TokenType.EQUAL | TokenType.GREAT | TokenType.LESS_EQUAL | TokenType.LESS_THAN | TokenType.DIFERENT:
                    solver = SolverRel()
                    res = solver.resolver(n)
                    print(f"{res}")
                case TokenType.AND | TokenType.OR:
                    solver = SolverLogic()
                    res = solver.resolver(n)
                    print(f"{res}")
                case TokenType.PRINT:
                    res = self.solverPrint(n)
                    print(f"{res}")
                    pass
                case TokenType.ASIGNATION:
                    self.solverAsig(n)
                    pass

    def resolverIf(self, n: Node):
        if n.children is None:
            if n.value.type == TokenType.NUMBER or n.value.type == TokenType.STRING:
                return n.value.literal
            elif n.value.type == TokenType.IDENTIFIER:
                return self.tsym.get(n.value.lexeme)

        condition = n.children[0]
        resultCondition = self.checkCond(condition)

        if n.children[-1].value.type == TokenType.ELSE:
            band = True
            body = n.children[1:]
            ebody = n.children[-1].children
        else:
            body = n.children[1:]
            band = False

        if resultCondition:
            root = Node(Token(TokenType.NULL, "", "", None))
            root.insertManyChildren(body)
            auxTree = Tree(root)
            auxTree.iterate()
        else:
            if band:
                root = Node(Token(TokenType.NULL, "", "", None))
                root.insertChildren(ebody)
                auxTree = Tree(root)
                auxTree.iterate()
            else:
                pass

    def solverWhile(self, n: Node):
        condition = n.children[0]
        body = n.children[1:]

        while self.checkCond(condition):
            root = Node(Token(TokenType.NULL, "", "", None))
            root.insertManyChildren(body)
            auxTree = Tree(root)
            auxTree.iterate()

    def solverFor(self, n: Node):
        initial = n.children[0]
        condition = n.children[1]
        increase = n.children[2]
        body = n.children[3:]

        self.solverVar(n.children[0])

        while self.checkCond(condition):
            root = Node(Token(TokenType.NULL, "", "", None))
            root.insertManyChildren(body)
            auxTree = Tree(root)
            auxTree.iterate()
            self.solverAsig(increase)

    def solverVar(self, n: Node):
        if len(n.children) == 1:
            if self.tsym.existsIdentifier(n.children[0].value.lexeme):
                print(f"{n.children[0].value.lexeme} ya existe")
                return
            self.tsym.asign(n.children[0].value.lexeme, None)
            return
        elif len(n.children) == 2:
            if self.tsym.existsIdentifier(n.children[0].value.lexeme):
                print(f"{n.children[0].value.lexeme} ya existe")
                return
            else:
                key = n.children[0].value.lexeme

            if self.posthelp.isOperator(n.children[1].value.type):
                operator = n.children[1].value.type
                if operator in (
                    TokenType.ADD,
                    TokenType.SUB,
                    TokenType.MULT,
                    TokenType.DIAG,
                ):
                    solver = SolverArithmetic()
                elif operator in (
                    TokenType.GREAT_EQUAL,
                    TokenType.EQUAL,
                    TokenType.GREAT,
                    TokenType.LESS_EQUAL,
                    TokenType.LESS_THAN,
                    TokenType.DIFERENT,
                ):
                    solver = SolverRelational()
                elif operator in (TokenType.AND, TokenType.OR):
                    solver = SolverLogic()
                else:
                    print("Operador no válido")
                    return

                value = solver.resolver(n.children[1])
            elif n.children[1].value.type == TokenType.IDENTIFIER:
                if self.tsym.existsIdentifier(n.children[1].value.lexeme):
                    value = self.tsym.get(n.children[1].value.lexeme)
                else:
                    print(f"{n.children[1].value.lexeme} no existe")
                    sys.exit()
            else:
                value = n.children[1].value.literal

            self.tsym.asign(key, value)
            return
        else:
            print("Error al declarar la variable")
            return None

    def solverAsig(self, n: Node):
        if self.tsym.existsIdentifier(n.children[0].value.lexeme):
            if n.children[0].value.type == TokenType.IDENTIFIER:
                if self.posthelp.isOperator(n.children[1].value.type):
                    operator = n.children[1].value.type
                    if operator in (
                        TokenType.ADD,
                        TokenType.SUB,
                        TokenType.MULT,
                        TokenType.DIAG,
                    ):
                        solver = SolverArithmetic()
                    elif operator in (
                        TokenType.GREAT_EQUAL,
                        TokenType.EQUAL,
                        TokenType.GREAT,
                        TokenType.LESS_EQUAL,
                        TokenType.LESS_THAN,
                        TokenType.DIFERENT,
                    ):
                        solver = SolverRelational()
                    elif operator in (TokenType.AND, TokenType.OR):
                        solver = SolverLogic()
                    else:
                        print("Operador no válido")
                        return

                    value = solver.resolver(n.children[1])
                    self.tsym.reasign(n.children[0].value.lexeme, value)
                    return
                else:
                    self.tsym.reasign(
                        n.children[0].value.lexeme, n.children[1].value.literal
                    )
                    return
        else:
            print(f"La variable {n.children[0].value.lexeme} no existe")
            return

    def solverPrint(self, n: Node):
        if n.children is None:
            if n.value.type == TokenType.NUMBER or n.value.type == TokenType.STRING:
                return n.value.literal
            elif n.value.type == TokenType.IDENTIFIER:
                return ts.simbolos.obtener(n.value.lexeme)

        child: Nodo = n.children[0]

        if self.posthelp.isOperator(child.value.type):
            match child.value.type:
                case TokenType.ADD | TokenType.SUB | TokenType.MULT | TokenType.DIAG:
                    solver = SolverArithmetic()
                    res = solver.resolver(child)
                    return res
                case TokenType.AND | TokenType.OR:
                    # print("jeje")
                    solver = SolverLogic()
                    res = solver.resolver(child)
                    return res
                case TokenType.GREAT_EQUAL | TokenType.EQUAL | TokenType.GREAT | TokenType.LESS_EQUAL | TokenType.LESS_THAN | TokenType.DIFERENT:
                    solver = SolverRel()
                    res = solver.resolver(child)
                    return res
        else:
            value = self.solverPrint(child)
            return value

    def checkCond(self, condition: Node) -> bool:
        if condition.value.type in (
            TokenType.GREAT_EQUAL,
            TokenType.EQUAL,
            TokenType.GREAT,
            TokenType.LESS_EQUAL,
            TokenType.LESS_THAN,
            TokenType.DIFERENT,
        ):
            solver = SolverRelational()
            resultCondition = solver.resolver(condition)
            return resultCondition
        elif condition.value.type in (TokenType.AND, TokenType.OR):
            solver = SolverLogic()
            resultCondition = solver.resolver(condition)
            return resultCondition
        elif condition.value.type == TokenType.TRUE:
            resultCondition = True
            return resultCondition
        elif condition.value.type == TokenType.FALSE:
            resultCondition = False
            return resultCondition
        elif condition.value.type == TokenType.IDENTIFIER:
            if self.tsym.existsIdentifier(condition.value.lexeme):
                if isinstance(self.tsym.get(condition.value.lexeme), bool):
                    resultCondition = self.tsym.get(condition.value.lexeme)
                    return resultCondition
                else:
                    print("La variable evaluada no es un boleano.\n")
                    sys.exit()
            else:
                print(f"La variable {condition.value.lexeme} no existe.\n")
                sys.exit()
        else:
            print("El resultado debe ser un boleano")
            sys.exit()
