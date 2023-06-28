from tokenType import TokenType
from tokens import Token
from node import Node
from postfixedGenerator import Postfixed
import symbolsTable as ts
from solverRelational import SolverRelational
from solverArithmetic import SolverArithmetic
from solverLogic import SolverLogic
import sys


class Tree:
    def __init__(self, root: Node) -> None:
        self.root = root
        self.posthelp = Postfixed([])

    def iterate(self):
        for index, n in enumerate(self.root.children):
            t = n.value
            match t.type:
                case TokenType.ADD| TokenType.SUB| TokenType.MULT| TokenType.DIAG:
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
                    solver = SolverRelational()
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
                return ts.SymbolsTable.get(n.value.lexeme)

        cond = n.children[0]
        rcond = self.checkCond(cond)

        if n.children[-1].value.type == TokenType.ELSE:
            el = True
            body = n.children[1:]
            ebody = n.children[-1].children
        else:
            body = n.children[1:]
            el = False

        if rcond:
            root = Node(Token(TokenType.NULL, "", "", None))
            root.insertManyChildren(body)
            araux = Tree(root)
            araux.iterate()
        else:
            if el:
                root = Node(Token(TokenType.NULL, "", "", None))
                root.insertManyChildren(ebody)
                araux = Tree(root)
                araux.iterate()
            else:
                pass

    def solverWhile(self, n: Node):
        cond = n.children[0]
        body = n.children[1:]

        while self.checkCond(cond):
            root = Node(Token(TokenType.NULL, "", "", None))
            root.insertManyChildren(body)
            araux = Tree(root)
            araux.iterate()

    def checkCond(self, cond: Node) -> bool:
        match cond.value.type:
            case TokenType.GREAT_EQUAL | TokenType.EQUAL | TokenType.GREAT | TokenType.LESS_EQUAL | TokenType.LESS_THAN | TokenType.DIFERENT:
                solver = SolverRelational()
                rcond = solver.resolver(cond)
                return rcond
            case TokenType.AND | TokenType.OR:
                solver = SolverLogic()
                rcond = solver.resolver(cond)
                return rcond
            case TokenType.TRUE:
                rcond = True
                return rcond
            case TokenType.FALSE:
                rcond = False
                return rcond
            case TokenType.IDENTIFIER:
                if ts.symbols.existsIdentifier(cond.value.lexeme):
                    if isinstance(ts.symbols.get(cond.value.lexeme), bool):
                        rcond = ts.symbols.get(cond.value.lexeme)
                        return rcond
                    else:
                        print("Error la variable evaluada no es un boleano.\n")
                        sys.exit()
                else:
                    print(f"Error: La variable {cond.value.lexeme} no existe.\n")
                    sys.exit()
            case _:
                print("Error: El resultado debe ser un boleano")
                sys.exit()

    def solverFor(self, n: Node):
        ini = n.children[0]
        cond = n.children[1]
        increase = n.children[2]
        body = n.children[3:]

        self.solverVar(n.children[0])

        while self.checkCond(cond):
            root = Node(Token(TokenType.NULL, "", "", None))
            root.insertManyChildren(body)
            araux = Tree(root)
            araux.iterate()
            self.solverAsig(increase)

        pass

    def solverVar(self, n: Node):
        if len(n.children) == 1:
            if ts.symbols.existsIdentifier(n.value.lexeme):
                print(f"Error: La variable {n.children[0].value.lexeme} ya existe")
                return
            ts.symbols.asign(n.children[0].value.lexeme, None)
            return
        elif len(n.children) == 2:
            if ts.symbols.existsIdentifier(n.children[0].value.lexeme):
                print(f"Error: La variable {n.children[0].value.lexeme} ya existe")
                return
            else:
                key = n.children[0].value.lexeme

            if self.posthelp.isOperator(n.children[1].value.type):
                match n.children[1].value.type:
                    case TokenType.ADD | TokenType.SUB | TokenType.MULT | TokenType.DIAG:
                        solver = SolverArithmetic()
                        value = solver.resolver(n.children[1])
                    case TokenType.GREAT_EQUAL | TokenType.EQUAL | TokenType.GREAT | TokenType.LESS_EQUAL | TokenType.LESS_THAN | TokenType.DIFERENT:
                        solver = SolverRelational()
                        value = solver.resolver(n.children[1])
                    case TokenType.AND | TokenType.OR:
                        solver = SolverLogic()
                        value = solver.resolver(n.children[1])
            elif n.children[1].value.type == TokenType.IDENTIFIER:
                if ts.symbols.existsIdentifier(n.children[1].value.lexeme):
                    value = ts.symbols.get(n.children[1].value.lexeme)
                    pass
                else:
                    print(
                        f"Error: La variable {n.children[1].value.lexeme} no existe, por lo cual no puede ser asignada a {n.children[0].value.lexeme}\n"
                    )
                    sys.exit()

            else:
                value = n.children[1].value.literal
            ts.symbols.asign(key, value)
            return
        else:
            print("Error al declarar la variable")
            return None

    def solverAsig(self, n: Node):
        if ts.symbols.existsIdentifier(n.children[0].value.lexeme):
            if n.children[0].value.type == TokenType.IDENTIFIER:
                if self.posthelp.isOperator(n.children[1].value.type):
                    match n.children[1].value.type:
                        case TokenType.ADD| TokenType.SUB| TokenType.MULT| TokenType.DIAG:
                            solver = SolverArithmetic()
                            value = solver.resolver(n.children[1])
                        case TokenType.GREAT_EQUAL | TokenType.EQUAL | TokenType.GREAT | TokenType.LESS_EQUAL | TokenType.LESS_THAN | TokenType.DIFERENT:
                            solver = SolverRelational()
                            value = solver.resolver(n.children[1])
                        case TokenType.AND | TokenType.OR:
                            solver = SolverLogic()
                            value = solver.resolver(n.children[1])
                    ts.symbols.reasign(n.children[0].value.lexeme, value)
                    return
                else:
                    ts.symbols.reasign(n.children[0].value.lexeme, n.children[1].value.literal)
                    return
        else:
            print(f"Error: La variable {n.children[0].value.lexeme} no existe")
            return

    def solverPrint(self, n: Node):
        if n.children is None:
            if n.value.type == TokenType.NUMBER or n.value.type == TokenType.STRING:
                return n.value.literal
            elif n.value.type == TokenType.IDENTIFIER:
                return ts.symbols.get(n.value.lexeme)

        child: Node = n.children[0]

        if self.posthelp.isOperator(child.value.type):
            match child.value.type:
                case TokenType.ADD | TokenType.SUB | TokenType.MULT | TokenType.DIAG:
                    solver = SolverArithmetic()
                    res = solver.resolver(child)
                    return res
                case TokenType.AND | TokenType.OR:
                    solver = SolverLogic()
                    res = solver.resolver(child)
                    return res
                case TokenType.GREAT_EQUAL | TokenType.EQUAL | TokenType.GREAT | TokenType.LESS_EQUAL | TokenType.LESS_THAN | TokenType.DIFERENT:
                    solver = SolverRelational()
                    res = solver.resolver(child)
                    return res
        else:
            valor = self.solverPrint(child)
            return valor
