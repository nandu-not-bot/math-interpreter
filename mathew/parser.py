from .utils import TT, BinaryOpNode, CMDNode, NumberNode, Token, ResultHandler, UnaryOpNode

class Parser:
    def __init__(self, toks: list[Token]):
        self.tokens = toks
        self.tok_idx = 0

    @property
    def current_tok(self):
        return self.tokens[self.tok_idx] if self.tok_idx < len(self.tokens) else None

    def advance(self):
        self.tok_idx += 1

    def parser(self):
        return self.expr()

    def expr(self):
        res = ResultHandler()
        term = res.register(self.term())
        if res.error:
            return res
        return res.success(term)

    def term(self):
        return self.bin_op(self.factor, (TT.PLUS, TT.MINUS))

    def factor(self):
        return self.bin_op(self.power, (TT.MULT, TT.DIV))

    def power(self):
        return self.bin_op(self.atom, (TT.POW,))

    def atom(self):  # sourcery skip: remove-redundant-if
        res = ResultHandler()

        if self.current_tok.type == TT.LPAR:
            self.advance()

            expr = res.register(self.expr())
            if res.error:
                return res

            if self.current_tok.type != TT.RPAR:
                return res.failure("Expected ')'")
            self.advance()

            if self.current_tok.type in (TT.NUM, TT.LPAR):
                atom = res.register(self.atom())
                if res.error: return res

                return res.success(BinaryOpNode(expr, Token(TT.MULT), atom))

            return res.success(expr)
        
        elif self.current_tok.type == TT.ABS:
            self.advance()

            expr = res.register(self.expr())
            if res.error:
                return res

            if self.current_tok.type != TT.ABS:
                return res.failure("Expected '|'")
            self.advance()

            return res.success(UnaryOpNode(Token(TT.ABS), expr))

        elif self.current_tok.type in (TT.PLUS, TT.MINUS):
            op_tok = self.current_tok
            self.advance()

            expr = res.register(self.expr())
            if res.error:
                return res

            if self.current_tok.type in (TT.NUM, TT.LPAR):
                atom = res.register(self.atom())
                if res.error: return res

                return res.success(BinaryOpNode(expr, Token(TT.MULT), atom))

            return res.success(UnaryOpNode(op_tok, expr))

        elif self.current_tok.type == TT.NUM:
            ret_val = NumberNode(self.current_tok)
            self.advance()

            if self.current_tok.type == TT.LPAR:
                atom = res.register(self.atom())
                if res.error: return res

                return res.success(BinaryOpNode(ret_val, Token(TT.MULT), atom))

            return res.success(ret_val)

        else:
            return res.failure(f"Invlid Syntax at '{self.current_tok}'")

    def bin_op(self, func_a: Token, op_toks: list[Token], func_b: Token = None):
        res = ResultHandler()

        if not func_b:
            func_b = func_a

        left = res.register(func_a())
        if res.error:
            return res

        while self.current_tok and (
            self.current_tok.type in op_toks
            or (self.current_tok.type, self.current_tok.value) in op_toks
        ):
            op_tok = self.current_tok
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res

            left = BinaryOpNode(left, op_tok, right)

        return res.success(left)
