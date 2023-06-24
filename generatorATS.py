from tokenType import TokenType
from tokens import Token
from tree import Tree
from node import Node

class GeneratorAST:
    def __init__(self, postfixed: list[Token]) -> None:
        self.postfixed = postfixed
        self.stack = [Node]

    def generateAST(self):
        parentStack = list[Node]
        root = Node(None)
        parentStack.append(root)
        parent: Node = root

        for token in self.postfixed:
            if token.type == TokenType.EOF: 
                pass

            if token.isRevervedWord():
                node = Node(token)
                parent = parentStack[-1]
                parent.insertNextChild(node)
                parentStack.append(node)
                parent = node;
            elif token.isOperating():
                node = None(token)
                self.stack.append(node)
            elif token.isOperator():
                aridad = token.aridad(token)
                node = Node(token)
                for i in aridad:
                    auxNode = self.stack.pop()
                    node.insertChild(auxNode)
                self.stack.append(node)
            elif token.type == TokenType.SEMICOLON:
                if len(self.stack) == 0:
                    # Si la pila está vcacía es porque token es un ; que cierra una estrctura de control
                    parentStack.pop()
                    padre = parentStack[-1]
                else:
                    node = self.stack.pop()
                    if node.getValue().type == TokenType.VAR:
                        # En el caso de VAR, es necesario eliminr el igual que pudiera aparecer en la razíz del nodo
                        if node.getValue().type == TokenType.EQUAL:
                            parent.insertChild
            
        