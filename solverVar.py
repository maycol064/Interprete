from tokenType import TokenType
from tokens import Token
from symbolsTable import SymbolsTable
from node import Node
import sys


class SolverVar:
    def __init__(self, node: Node):
        self.node: Node = node
        self.tsym = SymbolsTable()

    def resolver(self):
        self._resolver(self.node)

    def _resolver(self, node: Node):
        if len(self.nodo.children) == 2:
            key, value = "", 0
            for i in self.node.children:
                if i.value.type == TokeType.IDENTIFIER:
                    key = i.value.lexeme
                if self.tsym.existsIdentifier(key):
                    print(f"Error, {key} ya estaba definida")
                    sys.exit()
                elif (
                    (i.value.type == TokeType.NUMBER)
                    or (i.value.type == TokeType.STRING)
                    or (i.value.type == TokeType.TRUE)
                    or (i.value.type == TokeType.FALSE)
                ):
                    value = i.value.literal
            self.tsym.asign(key, value)
            return
        elif len(self.nodo.children) == 1:
            if self.node.children[0].value.type == TokeType.IDENTIFIER:
                key = self.node.children[0].value.lexeme
                if ts.simbolos.obtener(key):
                    print(f"Error: La variable {key} ya estaba definida")
                    sys.exit()
                ts.simbolos.asignar(key, None)
                return
        else:
            print("Error al declarar la variable")
            sys.exit()
