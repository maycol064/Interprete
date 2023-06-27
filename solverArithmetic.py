from node import Node
from tokenType import TokenType
from symbolsTable import SymbolsTable


class SolverArithmetic():
    def __init__(self):
        self.tsym = SymbolsTable()

    def resolver(self, node: Node):
        if node.getChildren() is None:
            if (
                node.getValue().type == TokenType.NUMBER
                or node.getValue().type == TokenType.STRING
            ):
                return node.getValue().literal
            elif node.getValue().type == TokenType.IDENTIFIER:
                # Ver tabla de símbolos
                pass

        # Por simplicidad se asume que la lista de hijos del nodo tiene dos elementos
        left = node.getChildren()[0]
        right = node.getChildren()[1]
        leftResult = self.resolver(left)
        rightResult = self.resolver(right)

        if isinstance(leftResult, float) and isinstance(rightResult, float):
            if node.getValue().type == TokenType.ADD:
                return leftResult + rightResult
            elif node.getValue().type == TokenType.SUB:
                return leftResult - rightResult
            elif node.getValue().type == TokenType.MULT:
                return leftResult * rightResult
            elif node.getValue().type == TokenType.DIAG:
                return leftResult / rightResult
        if isinstance(leftResult, str) and isinstance(rightResult, str):
            return f"{leftResult} {rightResult}"
        else:
            raise RuntimeError(f"Diferencia de tipos: {node.getValue().line}")
        return None
