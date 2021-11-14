from .utils import TT, TOK_VALS, ResultHandler, Token

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.current_idx = 0

    @property
    def current_char(self):
        return self.text[self.current_idx] if self.current_idx < len(self.text) else None

    def advance(self):
        self.current_idx += 1

    @property
    def turn(self):
        return self.text[self.current_idx - 1] if self.current_idx > 0 else None

    def make_toks(self):
        res = ResultHandler()
        tokens = []

        while self.current_char is not None:
        
            match self.current_char:

                case " ":
                    self.advance()

                case char if char.lower() in TOK_VALS:
                    tokens.append(Token(TOK_VALS[char]))
                    self.advance()

                case char if char in "1234567890.":
                    num = res.register(self.make_num())
                    if res.error: 
                        return res
                    tokens.append(num)
                
                case char:
                    return res.failure(f"Unexpected Character '{char}'")

        return res.success(tokens + [Token(TT.EOF)])

    def make_num(self):
        res = ResultHandler()
        num_str = ""

        while self.current_char and self.current_char in "1234567890. e+-":
            if self.current_char == " ":
                return res.failure(f"Unexpected spacing in after '{num_str[-1]}'")
            elif self.current_char == "." and ("." in num_str or "e" in num_str):
                return res.failure(f"Unexpected '.' after '{num_str[-1]}'")
            elif self.current_char == "e" and "e" in num_str:
                return res.failure(f"Unexpected 'e' after '{num_str[-1]}'")
            elif self.current_char in "+-" and num_str and self.turn != "e":
                return res.success(Token(TT.NUM, float(num_str+"0") if "." in num_str or "e" in num_str else int(num_str)))

            num_str += self.current_char
            self.advance()

        if num_str == ".":
            return res.failure("Unexpected Character '.'")

        return res.success(Token(
            TT.NUM,
            float(num_str) if "." in num_str or "e" in num_str else int(num_str)
        ))
