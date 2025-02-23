import re
from enum import Enum, auto

class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    OPERATOR = auto()
    SYMBOL = auto()
    EOF = auto()

KEYWORDS = {"var", "int", "string", "if", "import", "put"}
OPERATORS = {"=", "+", "-", "*", "/", ">", "<"}
SYMBOLS = {";", "(", ")", "{", "}"}

TOKEN_REGEX = [
    (TokenType.KEYWORD, r'\b(?:var|int|string|if|import|put)\b'),
    (TokenType.IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_]*'),
    (TokenType.NUMBER, r'\b\d+\b'),
    (TokenType.STRING, r'"[^"]*"'),
    (TokenType.OPERATOR, r'[=+\-*/><]'),
    (TokenType.SYMBOL, r'[;(){}]'),
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

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.next_token()

    def next_token(self):
        """Advance to the next token."""
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, expected_type):
        """Consume the current token if it matches the expected type."""
        if self.current_token is None:
            raise SyntaxError("Unexpected end of input")
        
        if self.current_token.type == expected_type:
            self.next_token()
        else:
            raise SyntaxError(f"Expected {expected_type} but got {self.current_token}")

    def require_semicolon(self):
        """Require a semicolon at the end of a statement."""
        if self.current_token and self.current_token.value == ";":
            self.eat(TokenType.SYMBOL)
        else:
            raise SyntaxError("Missing semicolon")

    def parse(self):
        """Main parse function to process all statements."""
        while self.current_token is not None:
            self.parse_statement()

    def parse_statement(self):
        """Parses a single statement."""
        print(f"DEBUG: Parsing statement {self.current_token}")  # Debugging line

        if self.current_token.value == "import":
            self.parse_import()
        elif self.current_token.value == "var":
            self.parse_variable_declaration()
        elif self.current_token.value == "if":
            self.parse_if_statement()
        elif self.current_token.value == "put":
            self.parse_put()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def parse_import(self):
        """Handles 'import' statements."""
        self.eat(TokenType.KEYWORD)  # Eat 'import'
        self.eat(TokenType.SYMBOL)
        self.eat(TokenType.IDENTIFIER)  # Eat module name
        self.eat(TokenType.SYMBOL)
        self.require_semicolon()
        print("Parsed import statement")

    def parse_variable_declaration(self):
        """Handles variable declaration."""
        self.eat(TokenType.KEYWORD)  # Eat 'var'

        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)  # Eat variable name

        var_type = self.current_token.value
        if var_type not in {"int", "float", "string"}:
            raise SyntaxError(f"Invalid type: {var_type}")
        self.eat(TokenType.KEYWORD)  # Eat type

        self.eat(TokenType.OPERATOR)  # Eat '='

        var_value = self.current_token.value
        if var_type == "int":
            self.eat(TokenType.NUMBER)
        elif var_type == "string":
            self.eat(TokenType.STRING)
        else:
            raise TypeError(f"Type mismatch: Expected {var_type} but got {var_value}")

        self.require_semicolon()
        print(f"Parsed variable declaration: {var_name} ({var_type}) = {var_value}")
        return var_name, var_type, var_value  # Correct order!

    def parse_if_statement(self):
        """Handles 'if' statements."""
        self.eat(TokenType.KEYWORD)  # Eat 'if'
        self.eat(TokenType.SYMBOL)  # Eat '('

        # Parse condition inside parentheses
        while self.current_token.type != TokenType.SYMBOL or self.current_token.value != ")":
            self.eat(self.current_token.type)

        self.eat(TokenType.SYMBOL)  # Eat ')'

        # Handle block with '{' or single statement
        if self.current_token.value == "{":
            self.eat(TokenType.SYMBOL)  # Eat '{'
            while self.current_token is not None and self.current_token.value != "}":
                self.parse_statement()
            self.eat(TokenType.SYMBOL)  # Eat '}'
        else:
            self.parse_statement()

        print("Parsed if statement")

    def parse_put(self):
        """Handles 'put' statements (print)."""
        self.eat(TokenType.KEYWORD)  # Eat 'put'

        if self.current_token.type == TokenType.STRING:
            output_value = self.current_token.value
            self.eat(TokenType.STRING)  # Eat string value
        elif self.current_token.type == TokenType.IDENTIFIER:
            output_value = self.current_token.value  # Just return the variable name
            self.eat(TokenType.IDENTIFIER)  # Eat variable name
        else:
            raise SyntaxError(f"Invalid 'put' argument: {self.current_token}")

        self.require_semicolon()
        print(f"DEBUG: Parsed put statement: {output_value}")  # Debugging output
        return output_value  # Return the variable name (if identifier)

class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.variables = {}

    def interpret(self):
        while self.parser.current_token.type != TokenType.EOF:
            self.execute_statement()

    def execute_statement(self):
        token = self.parser.current_token

        if token.value == "import":
            self.execute_import()
        elif token.value == "var":
            self.execute_variable_declaration()
        elif token.value == "put":
            self.execute_put()
        elif token.value == "if":
            self.execute_if()
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def execute_import(self):
        self.parser.parse_import()

    def execute_variable_declaration(self):
        var_name, var_type, var_value = self.parser.parse_variable_declaration()
        
        print(f"DEBUG: Raw parsed values: {var_name} ({var_type}) = {var_value}")
    
        # Ensure var_value is not the type name ("int") by mistake
        if var_type == "int":
            try:
                var_value = int(var_value)  # Convert the value to an integer
            except ValueError:
                raise SyntaxError(f"Invalid integer value for variable {var_name}: {var_value}")
    
        # Store the actual value in the variable storage
        self.variables[var_name] = var_value
    
        print(f"DEBUG: Stored variable {var_name} = {self.variables[var_name]}")

    def execute_put(self):
        value = self.parser.parse_put()
        if value in self.variables:
            print(self.variables[value])  # Ensure variable values are printed
            return self.variables[value]  # Optional, useful for debugging
        else:
            print(value)

    def execute_if(self):
        self.parser.parse_if_statement()



code = '''
import {math};
var x int = 42;
if (x > 10) {
    put "Hello World!";
}
var y int = 50;
put x;
put y;
'''

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
interpreter = Interpreter(parser)

interpreter.interpret()
