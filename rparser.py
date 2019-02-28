from enum import Enum
from rlexer import TokenType
from rlexer import Token


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.main_node = None
        self.lines = []
        self.nodes = []

    def parse(self):
        self.lines = self.make_lines()
        for line in self.lines:
            expression = line.to_exp()
            # print(expression.contents)
            self.nodes.append(expression.to_nodes())
        self.merge_nodes()

        # self.main_node.print()
        return self.main_node

    def merge_nodes(self):
        self.main_node = self.nodes[0]
        for node in self.nodes[1:]:
            tabs = node.tabs
            parent = self.main_node
            for i in range(tabs - 1):
                parent = parent.children[-1]
            parent.add_child(node)
            node.set_parent(parent)
        self.main_node.set_level([])

    def make_lines(self):
        lines = []
        line = []
        for token in self.tokens:
            if token.token_type == TokenType.NEWLINE:
                lines.append(Line(line))
                line = []
            elif token.token_type != TokenType.WHITESPACE:
                line.append(token)
        return lines


class Node:
    def __init__(self, token, node_type):
        self.value = token.value
        self.token = token
        self.node_type = node_type
        self.children = []
        self.parent = None
        self.level = []
        self.tabs = None
        self.reg = None

    def set_reg(self, reg):
        self.reg = reg

    def add_child(self, child):
        self.children.append(child)

    def set_parent(self, parent):
        self.parent = parent

    def set_level(self, base, i=0):
        self.level += base
        self.level.append(i)
        for i, child in enumerate(self.children):
            child.set_level(self.level, i)

    def print(self):
        print(self.level, self.node_type.name, self.token.value)
        if self.children:
            for c in self.children:
                c.print()


class NodeType(Enum):
    ASSIGN = 0
    CALL = 1
    BIN = 2
    DECLARE = 3
    NUMBER = 4
    VARIABLE = 5


class Expression:
    def __init__(self):
        self.contents = []
        self.tabs = 0

    def __len__(self):
        return len(self.contents)

    def append(self, i):
        self.contents.append(i)

    def get_contents(self):
        return self.contents

    def __repr__(self):
        return self.contents.__repr__()

    def to_nodes(self):
        child_nodes = []
        node = None
        for element in self.contents:
            node_type = None
            if type(element) == Token:
                if len(self) == 2 and element.token_type == TokenType.IDENTIFIER and type(
                        self.contents[1]) == Expression:
                    node_type = NodeType.CALL
                elif element.token_type == TokenType.EQUAL:
                    node_type = NodeType.ASSIGN
                elif element.token_type == TokenType.BINARYOP:
                    node_type = NodeType.BIN
                elif element.token_type == TokenType.KEYWORD:
                    node_type = NodeType.DECLARE
                elif element.token_type == TokenType.NUMBER:
                    node_type = NodeType.NUMBER
                elif element.token_type == TokenType.IDENTIFIER:
                    node_type = NodeType.VARIABLE
                tmp_node = Node(element, node_type)
                if node_type == NodeType.NUMBER or node_type == NodeType.VARIABLE:
                    child_nodes.append(tmp_node)
                else:
                    node = tmp_node
            elif type(element) == Expression:
                tmp_node = element.to_nodes()
                child_nodes.append(tmp_node)
        if node is None:
            if child_nodes:
                node = child_nodes[0]
                child_nodes = []
            else:
                return None
        node.tabs = self.tabs
        for n in child_nodes:
            node.add_child(n)
            n.set_parent(node)
        return node


class Line:
    def __init__(self, line):
        self.line = line
        self.index = 0

    def has_next(self):
        return self.index < len(self.line)

    def next(self):
        self.index += 1
        return self.line[self.index - 1]

    def __repr__(self):
        return self.line.__repr__()

    def to_exp(self):
        exp = Expression()
        while self.has_next():
            element = self.next()
            if element.token_type == TokenType.TAB:
                exp.tabs += 1
            elif element.token_type == TokenType.RIGHTPAREN:
                print(exp)
                return exp
            elif element.token_type == TokenType.KEYWORD:
                exp.append(element)
            elif element.token_type == TokenType.IDENTIFIER:
                exp.append(element)
            elif element.token_type == TokenType.NUMBER:
                exp.append(element)
            elif element.token_type == TokenType.LEFTPAREN:
                next_exp = self.to_exp()
                if len(next_exp) != 0:
                    exp.append(next_exp)
            elif element.token_type == TokenType.BINARYOP or element.token_type == TokenType.EQUAL:
                next_exp = self.to_exp()
                exp.append(element)
                if len(next_exp) == 1:
                    exp.append(next_exp.get_contents()[0])
                    return exp
                elif len(next_exp) > 0:
                    exp.append(next_exp)
        print(exp)
        return exp


