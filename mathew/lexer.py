from .utils import CMDS, TT, TOK_VALS, ResultHandler, Token

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.current_idx = 0

    @property
    def current_char(self):
        return self.text[self.current_idx] if self.current_idx < len(self.text) else None

    def advance(self):
        self.current_idx += 1

    def make_toks(self):
        res = ResultHandler()
        tokens = []

        while self.current_char is not None:
        
            match self.current_char:

                case " ":
                    self.advance()

                case char if char in TOK_VALS:
                    tokens.append(Token(TOK_VALS[char]))
                    self.advance()

                case char if char in "1234567890.":
                    tokens.append(self.make_num())
                
                case char:
                    return res.failure(f"Unexpected Character '{char}'")

        return res.success(tokens + [Token(TT.EOF)])

    def make_num(self):
        num_str = ""

        while self.current_char and self.current_char in "1234567890. ":
            if self.current_char == " ":
                self.advance()
                continue 
            if self.current_char == ".":
                self.advance()
                if "." not in num_str:
                    num_str += "."
                continue

            num_str += self.current_char
            self.advance()

        return Token(
            TT.NUM,
            float(num_str) if "." in num_str else int(num_str)
        )
