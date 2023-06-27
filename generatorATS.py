from tokenType import TokenType
from tokens import Token
from tree import Tree
from node import Node
from postfixedGenerator import Postfixed


class GeneratorAST:
    def __init__(self, postfixed: list[Token]) -> None:
        self.postfixed = postfixed
        self.stack = []
        self.posthelp = Postfixed(None)

    def generateAST(self):
        parentStack = []
        root = Node(Token(TokenType.NULL, "", "", None))
        parentStack.append(root)
        parent: Node = root

        for i, t in enumerate(self.postfixed):
            if t.type == TokenType.EOF:
                break

            if t.type in self.posthelp.reserved_words.values():
                n = Node(t)
                parent = parentStack[-1]
                parent.insertNextChild(n)
                parentStack.append(n)
                parent = n
            elif self.posthelp.isOperating(t.type):
                n = Node(t)
                self.stack.append(n)
            elif self.posthelp.isOperator(t.type):
                aridad = self.posthelp.aridad(t.type)
                n = Node(t)
                for _ in range(aridad):
                    auxNode = self.stack.pop()
                    n.insertChild(auxNode)
                self.stack.append(n)
            elif t.type == TokenType.SEMICOLON:
                if len(self.stack) == 0:
                    parentStack.pop()
                    parent = parentStack[-1]
                else:
                    n = self.stack.pop()

                    if parent.value.type == TokenType.VAR:
                        if n.value.type == TokenType.ASIGNATION:
                            parent.insertManyChildren(n.children)
                        else:
                            parent.insertNextChild(n)
                        parentStack.pop()
                        parent = parentStack[-1]
                    elif parent.value.type == TokenType.PRINT:
                        parent.insertNextChild(n)
                        parentStack.pop()
                        parent = parentStack[-1]
                    else:
                        parent.insertNextChild(n)

        self.printTree(root)    
        
        result = Tree(root)
        return result

    def printTree(self, node: Node, level = 0):
        if node is None:
            return
        print(f"{' ' * level}{node.value}")
        if node.children:
            for i in node.children:
                self.printTree(i, level+1)