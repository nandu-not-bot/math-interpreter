import json

from .utils import TT, ResultHandler
from .parser import BinaryOpNode, UnaryOpNode, NumberNode

class Interpreter:
    def visit(self, node) -> ResultHandler:
        method = getattr(self, f"visit_{type(node).__name__}", "no_visit_method")
        return method(node)

    def no_visit_method(self, _):
        raise RuntimeError("We shouldn't even be here...")

    def visit_BinaryOpNode(self, node: BinaryOpNode):
        res = ResultHandler()

        op_tok = node.op_tok

        left_val = res.register(self.visit(node.left_node))
        if res.error: return res
        right_val = res.register(self.visit(node.right_node))
        if res.error: return res

        match op_tok.type:
            case TT.PLUS:
                return res.success(left_val + right_val)
            case TT.MINUS:
                return res.success(left_val - right_val)
            case TT.MULT:
                return res.success(left_val * right_val)
            case TT.DIV:
                if right_val == 0: return res.failure("Division by zero error")
                return res.success(left_val / right_val)
            case TT.POW:
                return res.success(left_val ** right_val)
            case _:
                return res.failure(f"Unsupported binary operation '{op_tok}'")

    def visit_UnaryOpNode(self, node: UnaryOpNode):
        res = ResultHandler()

        op_tok = node.op_tok

        val = res.register(self.visit(node.val_node))
        if res.error: return res

        match op_tok.type:
            case TT.MINUS:
                return res.success(-val)
            case TT.PLUS:
                return res.success(+val)
            case TT.ABS:
                return res.success(abs(val))
            case _:
                return res.failure(f"Unsupported unary operation '{op_tok}'")

    def visit_NumberNode(self, node: NumberNode):
        res = ResultHandler()
        if node.num.type == TT.NUM:
            return res.success(
                int(node.num.value) 
                if isinstance(node.num.value, int) 
                else float(node.num.value)
            )
        elif node.num.type == TT.R:
            with open("info.json", "r") as f:
                info = json.load(f)
            return res.success(info["r"])
