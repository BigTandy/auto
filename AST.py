from typing import Self
from classdefs import Compound


class toNode:
    """
    Node Cast
    """
    def __new__(self, other):
        ty = type(other)
        if ty == Compound:
            return Compound_Node(other)
        elif ty == str:
            if other == "PLUS":
                return Plus_Node()  #TODO Takes Args?
            elif other == "ARROW":
                return Arrow_Node()



class Node:
    """
    Base type in the AST
    """
    def __init__(self):
        self.children = set()

    def __add__(self, other: Self):
        self.children.add(other)



class Start_Node(Node):
    """
    Start Node in the AST
    """


class Compound_Node(Node):
    """
    Represents a compound in the AST
    """
    def __init__(self, compound: Compound):
        super().__init__()
        self.comp = compound


class Plus_Node(Node):
    """
    Represents a plus in the AST
    """
    def __init__(self, *args: Compound_Node):
        super().__init__()
        self.comps = []
        for _ in args:
            self.comps.append(_)


class Arrow_Node(Node):
    """
    Represents an arrow in the AST
    """
    def __init__(self):
        super().__init__()


















