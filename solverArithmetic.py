from node import Node
from tokenType import TokenType
import symbolsTable as ts
import sys


class SolverArithmetic:
    def __init__(self):
        pass

    def resolver(self, n: Node):
        if n.children is None:
            if n.value.type == TokenType.NUMBER or n.value.type == TokenType.STRING:
                return n.value.literal
            elif n.value.type == TokenType.IDENTIFIER:
                return ts.symbols.get(n.value.lexeme)
            else:
                return None

        nLeft: Nodo = n.children[0]
        nRigth: Nodo = n.children[1]

        resLeft = self.resolver(nLeft)
        resRigth = self.resolver(nRigth)

        if isinstance(resLeft, float) and isinstance(resRigth, float):
            match n.value.type:
                case TokenType.ADD:
                    return resLeft + resRigth
                case TokenType.SUB:
                    return resLeft - resRigth
                case TokenType.MULT:
                    return resLeft * resRigth
                case TokenType.DIAG:
                    return resLeft / resRigth
        elif isinstance(resLeft, str) and isinstance(resRigth, str):
            if n.value.type == TokenType.ADD:
                return resLeft + resRigth
        else:
            print(
                f"Error al realizar la operación. {n.value.type} es incompatible con {type(resLeft)} y {type(resRigth)}"
            )
            sys.exit()
        return None
