from enum import Enum
import re


class TokenType(Enum):
    WHITESPACE = "(?<=[^\\s\\\\]) (?=[^\\s\\\\])"
    NEWLINE = "[\n]+"
    TAB = "[\t]+|(\\\\G|^) {4}"
    LEFTPAREN = "\\("
    RIGHTPAREN = "\\)"
    COLON = "\\:"
    EQUAL = "(?<!=)=(?!=)"
    BINARYOP = "[*|/|+|-]"
    NUMBER = "[0-9]+"
    KEYWORD = "public|private|static|return|new"
    IDENTIFIER = "(\\w+)"


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return self.token_type.name + " (" + self.value + ")"


class Lexer:
    def __init__(self, data):
        self.data = data
        self.tokens = list()

    def lex(self):
        pos = 0
        while pos < len(self.data):
            for pattern, t in [[i.value, str(i)] for i in TokenType]:
                regex = re.compile(pattern)
                match = regex.match(self.data, pos)
                if match:
                    value = match.group(0)
                    if t:
                        self.tokens.append(Token(TokenType(pattern), value))
                    else:
                        print(value)
                        print(t)
                    pos = match.end(0)
                    break
            else:
                raise SyntaxError("Token not found: " + self.data[pos:])
        return self.tokens
