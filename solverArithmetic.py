from node import Node
from tokenType import TokenType
from symbolsTable import SymbolsTable


class SolverArithmetic:
    def __init__(self):
        self.tsym = SymbolsTable()

    def resolver(self, node: Node):
        if node.children is None:
            if n.value.type == TipoToken.NUMBER or n.value.type == TipoToken.STRING:
                return n.value.literal
            elif n.value.type == TipoToken.IDENTIFIER:
                return ts.simbolos.obtener(n.value.lexeme)
            else:
                return None

        leftNode: Nodo = node.children[0]
        rightNode: Nodo = node.children[1]

        leftRes = self.resolver(leftNode)
        rigthRes = self.resolver(rightNode)

        if isinstance(leftRes, float) and isinstance(rigthRes, float):
            match n.value.type:
                case TipoToken.ADD:
                    return leftRes + rigthRes
                case TipoToken.SUB:
                    return leftRes - rigthRes
                case TipoToken.MULT:
                    return leftRes * rigthRes
                case TipoToken.DIAG:
                    return leftRes / rigthRes
        elif isinstance(leftRes, str) and isinstance(rigthRes, str):
            if n.value.type == TipoToken.ADD:
                return leftRes + rigthRes
        else:
            print(
                f"Error: No se puede resolver la operacion {n.value.type} con las instancias {type(leftRes)} y {type(rigthRes)}"
            )
        return None
