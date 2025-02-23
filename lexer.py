import re
from enum import Enum, auto

__all__ = ["TokenType"]

class TokenType(Enum):
    KEYWORD = auto()      # for commands like 'var', 'put', 'if'
    IDENTIFIER = auto()   # for variable names
    NUMBER = auto()       # for integer values
    FLOAT = auto()        # for decimal numbers
    STRING = auto()       # for text
    BOOL = auto()         # for true/false
    LIST = auto()         # for lists
    DICT = auto()         # for key-value pairs
    TYPE = auto()         # NEW: For 'int', 'float', 'string', etc.
    OPERATOR = auto()     # for '=', '+', '-', '*', '/'
    SYMBOL = auto()       # for '{', '}', '(', ')', etc.
    EOF = auto()          # end of file

KEYWORDS = {"var", "if", "import", "put"}
OPERATORS = {"=", "+", "-", "*", "/", ">", "<"}
SYMBOLS = {";", "(", ")", "{", "}"}
TYPES = {"int", "float", "string", "bool", "list", "dict"}

TOKEN_REGEX = [
    (TokenType.KEYWORD, r'\b(?:var|if|import|put)\b'),  # Only commands
    (TokenType.TYPE, r'\b(?:int|float|string|bool|list|dict)\b'),  # Types
    (TokenType.BOOL, r'\b(?:true|false)\b'),
    (TokenType.FLOAT, r'\b\d+\.\d+\b'),
    (TokenType.NUMBER, r'\b\d+\b'),
    (TokenType.STRING, r'"[^"]*"'),
    (TokenType.OPERATOR, r'[=+\-*/><]'),
    (TokenType.SYMBOL, r'[;(){}[\]]'),  
]

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.pos = 0

    def tokenize(self):
        while self.pos < len(self.code):
            match = None
            for token_type, regex in TOKEN_REGEX:
                regex = re.compile(regex)
                match = regex.match(self.code, self.pos)
                if match:
                    value = match.group(0)
                    if token_type == TokenType.STRING:
                        value = value.strip('"')  # Remove quotes from strings
                    self.tokens.append(Token(token_type, value))
                    self.pos = match.end()
                    break
            if not match:
                if self.code[self.pos].isspace():
                    self.pos += 1  # Skip whitespace
                else:
                    raise SyntaxError(f"Unexpected character: {self.code[self.pos]}")
        self.tokens.append(Token(TokenType.EOF, "EOF"))
        return self.tokens
