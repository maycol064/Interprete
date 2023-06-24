from tokenType import TokenType
from tokens import Token
from tree import Tree
from node import Node

class GeneratorAST:
  def __init__(self, postfixed: list[Token]) -> None:
    self.postfixed = postfixed
    self.stack = []

  def generateAST(self):
    parentStack = list[Node]
    root = Node(None)
    parentStack.append(root)
    parent = root

    for token in self.postfixed:
      if token.type == TokenType.EOF: 
        pass
  