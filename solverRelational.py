from tokenType import TokenType
from tokens import Token
from node import Node
from symbolsTable import SymbolsTable
import sys
from postfixedGenerator import Postfixed
from solverArithmetic import SolverArithmetic


class SolverRelational:
    def __init__(self):
        self.posthelp = Postfixed([])
        self.tsym = SymbolsTable()
        pass

    def resolver(self, n: Node):
        if n.children is None:
            if (
                n.value.type == TokenType.NUMBER
                or n.value.type == TokenType.STRING
                or n.value.type == TokenType.TRUE
                or n.value.type == TokenType.FALSE
            ):
                return n.value.literal
            elif n.value.type == TokenType.IDENTIFIER:
                return self.tsym.get(n.value.lexeme)

        leftNode: Node = n.children[0]
        rightNode: Node = n.children[1]

        if self.posthelp.isOperator(leftNode.value.type) and self.posthelp.isOperator(
            rightNode.value.type
        ):
            resolverA = SolverArithmetic()
            leftResult = resolverA.resolver(leftNode)
            rightResult = resolverA.resolver(rightNode)
        elif self.posthelp.isOperator(leftNode.value.type):
            rightResult = self.resolver(rightNode)
            resolverA = SolverArithmetic()
            leftResult = resolverA.resolver(leftNode)
        elif self.posthelp.isOperator(rightNode.value.type):
            leftResult = self.resolver(leftNode)
            resolverA = SolverArithmetic()
            rightResult = sol.resolver(rightNode)
        else:
            leftResult = self.resolver(leftNode)
            rightResult = self.resolver(rightNode)

        if type(leftResult) == type(rightResult) and type(rightResult) == float:
            match n.value.type:
                case TokenType.GREAT:
                    return leftResult > rightResult
                case TokenType.GREAT_EQUAL:
                    return leftResult >= rightResult
                case TokenType.EQUAL:
                    return leftResult == rightResult
                case TokenType.LESS_THAN:
                    return leftResult < rightResult
                case TokenType.LESS_EQUAL:
                    return leftResult <= rightResult
                case TokenType.DIFERENT:
                    return leftResult != rightResult
        elif type(leftResult) == type(rightResult):
            if n.value.type == TokenType.EQUAL:
                return leftResult == rightResult
            else:
                print(
                    f"No se puede resolver la operacion {str(n.value.type)[10:]} con las instancias {type(leftResult)} y {type(rightResult)}"
                )
                sys.exit()
        else:
            print(
                f"Error: No se puede resolver la operacion {str(n.value.type)[10:]} con las instancias {type(leftResult)} y {type(rightResult)}"
            )
            sys.exit()
        return None
