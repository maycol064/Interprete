from tokenType import TokenType
from token import Token

class Node:
  def __init__(self, value: Token):
    self.value = value
    self.children = None
    pass

  def insertChild(self, child):
    if self.children is None:
      self.children = [child]
    else: 
      self.children.insert(0, child)

  def insertNextChild(self, child):
    if self.children is None:
      self.children = [child]
    else:
      self.children.append(child)

  def insertManyChildren(self, children):
    if self.children is None:
      self.children = []
    else: 
      self.children.extend(children)

  def getValue(self) -> Token:
    return self.value

  def getChildren(self) -> list[Node]:
    return self.children