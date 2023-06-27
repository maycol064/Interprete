from node import Node
from tokenType import TokenType
from symbolsTable import SymbolsTable


class SolverArithmetic:
    def __init__(self):
        self.tsym = SymbolsTable()

    def resolver(self, n: Node):
        if n.children is None:
            if n.value.type == TokenType.NUMBER or n.value.type == TokenType.STRING:
                return n.value.literal
            elif n.value.type == TokenType.IDENTIFIER:
                return ts.simbolos.obtener(n.value.lexeme)
            else:
                return None

        leftNode: Node = n.children[0]
        rightNode: Node = n.children[1]

        leftRes = self.resolver(leftNode)
        rigthRes = self.resolver(rightNode)

        if isinstance(leftRes, float) and isinstance(rigthRes, float):
            match n.value.type:
                case TokenType.ADD:
                    return leftRes + rigthRes
                case TokenType.SUB:
                    return leftRes - rigthRes
                case TokenType.MULT:
                    return leftRes * rigthRes
                case TokenType.DIAG:
                    return leftRes / rigthRes
        elif isinstance(leftRes, str) and isinstance(rigthRes, str):
            if n.value.type == TokenType.ADD:
                return leftRes + rigthRes
        else:
            print(
                f"Error: No se puede resolver la operacion {n.value.type} con las instancias {type(leftRes)} y {type(rigthRes)}"
            )
        return None
