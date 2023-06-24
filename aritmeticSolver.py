from node import Node
from tokenType import TokenType


class AritmeticSolver:
    def __init__(self, node: Node):
        this.node = node

    def resolver(self):
        return self._resolver(self.node)

    def _resolver(self, node: Node):
        if node.getChildren() is None:
            if node.getValue().type == TokenType.NUMBER or node.getValue().type == TokenType.STRING:
                return node.getValue().literal
            elif node.getValue().type == TokenType.IDENTIFIER:
                # Ver tabla de símbolos
                pass
        
        # Por simplicidad se asume que la lista de hijos del nodo tiene dos elementos
        left = node.getChildren()[0]
        right = node.getChildren()[1]
        leftResult = self._resolver(left)
        rightResult = self._resolver(right)

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
            return f'{leftResult} {rightResult}'
        else:
            raise RuntimeError(f'Error: diferencia de tipos: {node.getValue().line}')
    return None
