from tokenType import TokenType
from token import Token
from node import Node

class Tree:
  def __init__(self, root: Node) -> None:
    self.root = root

  def iterate(self):
    for index, n in enumerate(self.root.children):
      top = n.value
      match top.type:
        case TokenType.ADD, TokenType.SUB, TokenType.MULT, TokenType.DIAG:
          pass
        case TokenType.VAR:
          ### Create a variable, use symbols table
          pass
        case IF:
          pass