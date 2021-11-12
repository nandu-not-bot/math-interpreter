from enum import Enum, auto


class TT(Enum):
    PLUS = auto()
    MINUS = auto()
    MULT = auto()
    DIV = auto()
    POW = auto()
    NUM = auto()
    ABS = auto()
    LPAR = auto()
    RPAR = auto()
    EOF = auto()


class Token:
    def __init__(self, type: TT, value=None):
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return f"{self.type}:{self.value}" if self.value is not None else f"{self.type}"


class ResultHandler:
    node = None
    error = None

    def register(self, res):
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error:
            self.error = error
        return self


class BinaryOpNode:
    def __init__(self, left_node: Token, op_tok: Token, right_node: Token):
        self.left_node = left_node
        self.right_node = right_node
        self.op_tok = op_tok

    def __repr__(self):
        return f"b({self.left_node} {self.op_tok} {self.right_node})"


class UnaryOpNode:
    def __init__(self, op_tok: Token, num_tok: Token):
        self.op_tok = op_tok
        self.val_node = num_tok

    def __repr__(self):
        return f"u({self.op_tok.value} {self.val_node})"


class NumberNode:
    def __init__(self, num: Token, is_neg: bool = False):
        self.num = num
        self.is_neg = is_neg

    def __repr__(self):
        return str(self.num)


TOK_VALS = {
    "+": TT.PLUS,
    "-": TT.MINUS,
    "*": TT.MULT,
    "/": TT.DIV,
    "^": TT.POW,
    "|": TT.ABS,
    "(": TT.LPAR,
    ")": TT.RPAR,
}
