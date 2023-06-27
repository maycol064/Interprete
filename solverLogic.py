from tokenType import TokenType
from node import Node
from symbolsTable import SymbolsTable
import sys
from postfixedGenerator import Postfixed
from solverRelational import SolverRelational


class SolverLogic:
    def __init__(self) -> None:
        self.posthelp = Postfix([])
        self.tsym = SymbolsTable()
        pass

    def resolver(self, n: Node):
        if n.children is None:
            if n.value.type == TokenType.TRUE or n.value.type == TokenType.FALSE:
                return n.value.literal
            elif n.value.type == TokenType.IDENTIFIER:
                return self.tsym.get(n.value.lexeme)
            else:
                return None

        leftNode: Node = n.children[0]
        rightNode: Node = n.children[1]

        if self.posthelp.isOperator(leftNode.value.type) and self.posthelp.isOperator(
            rightNode.value.type
        ):
            sol = SolverRelational()
            leftResult = sol.resolver(leftNode)
            rightResul = sol.resolver(rightNode)
        elif self.posthelp.isOperator(leftNode.value.type):
            rightResul = self.resolver(rightNode)
            sol = SolverRelational()
            leftResult = sol.resolver(leftNode)
        elif self.posthelp.isOperator(rightNode.value.type):
            leftResult = self.resolver(leftNode)
            sol = SolverRelational()
            rightResul = sol.resolver(rightNode)
        else:
            leftResult = self.resolver(leftNode)
            rightResul = self.resolver(rightNode)

        if isinstance(leftResult, bool) and isinstance(rightResul, bool):
            match n.value.type:
                case TokenType.AND:
                    return leftResult and rightResul
                case TokenType.OR:
                    return leftResult or rightResul
        else:
            print(
                f"No se puede realizar la operacion {str(n.value.type)[10:]} con las instancias {leftResult} y {rightResul}"
            )
