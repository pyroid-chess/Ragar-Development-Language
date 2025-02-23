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

from lexer import TokenType

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
        print(f"{self.current_token}")  # Debugging line

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
        mod = self.current_token.value  # Get module name
        self.eat(TokenType.SYMBOL) # {
        self.eat(TokenType.IDENTIFIER)  # Eat module name
        self.eat(TokenType.SYMBOL) # }
        self.require_semicolon()  # Ensure ';' is present
        print(f"Imported: {mod}")  # Print actual module name
        return mod  # Optionally return the module name for further processing

    def parse_variable_declaration(self):
        """Parses variable declarations like 'var x int = 5;'"""
        self.eat(TokenType.KEYWORD)  # Eat 'var'
        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)  # Eat variable name
        
        if self.current_token.type != TokenType.TYPE:
            raise SyntaxError(f"Expected a type, but got {self.current_token}")
    
        var_type = self.current_token.value
        self.eat(TokenType.TYPE)  # Eat the type (int, float, etc.)
    
        self.eat(TokenType.OPERATOR)  # Eat '='
    
        if var_type == "int":
            value = int(self.current_token.value)
            self.eat(TokenType.NUMBER)
    
        elif var_type == "float":
            value = float(self.current_token.value)
            self.eat(TokenType.FLOAT)
    
        elif var_type == "string":
            value = self.current_token.value.strip('"')
            self.eat(TokenType.STRING)
    
        elif var_type == "bool":
            value = self.current_token.value == "true"
            self.eat(TokenType.BOOL)
    
        elif var_type == "list":
            value = self.parse_list()
    
        elif var_type == "dict":
            value = self.parse_dict()
    
        else:
            raise SyntaxError(f"Unknown data type: {var_type}")
    
        self.require_semicolon()
        self.variables[var_name] = value
        return var_name, value

    def parse_if_statement(self):
        """Handles 'if' statements with proper condition evaluation."""
        self.eat(TokenType.KEYWORD)  # Eat 'if'
        self.eat(TokenType.SYMBOL)   # Eat '('
    
        # Collect tokens for the condition
        condition_tokens = []
        while self.current_token.type != TokenType.SYMBOL or self.current_token.value != ")":
            condition_tokens.append(self.current_token)
            self.eat(self.current_token.type)
    
        self.eat(TokenType.SYMBOL)   # Eat ')'
        
        # Convert condition tokens to a string
        condition_str = " ".join(token.value for token in condition_tokens)
        print(f"DEBUG: Parsed Condition: {condition_str}")  # Debugging
    
        return condition_tokens  # Pass tokens to Interpreter for evaluation

    def parse_put(self):
        """Handles 'put' statements (print)."""
        self.eat(TokenType.KEYWORD)  # Eat 'put'

        if self.current_token.type == TokenType.SYMBOL and self.current_token.value == "{":
            self.eat(TokenType.SYMBOL)  # Eat '{'

            if self.current_token.type == TokenType.STRING:
                output_value = self.current_token.value
                self.eat(TokenType.STRING)  # Eat string value
            elif self.current_token.type == TokenType.IDENTIFIER:
                output_value = self.current_token.value  # Just return the variable name
                self.eat(TokenType.IDENTIFIER)  # Eat variable name
            else:
                raise SyntaxError(f"Invalid 'put' argument: {self.current_token}")

            if self.current_token.type == TokenType.SYMBOL and self.current_token.value == "}":
                self.eat(TokenType.SYMBOL)  # Eat '}'
            else:
                raise SyntaxError("Expected '}' after put argument")

        else:
            raise SyntaxError("Expected '{' after 'put'")

        self.require_semicolon()
        print(f"{output_value}")  # Debugging output
        return output_value  # Return the variable name (if identifier)

from lexer import TokenType
class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.variables = {}

    def interpret(self):
        while self.parser.current_token.type != TokenType.EOF:
            self.execute_statement()
            
    def evaluate_condition(self, condition_str):
        """Evaluates a parsed condition expression using interpreter's variables."""
        try:
            # Check if variables exist in interpreter
            variables = {var: self.variables[var] for var in self.variables}

            # Evaluate condition safely
            return eval(condition_str, {}, variables)

        except Exception as e:
            print(f"DEBUG: Condition Evaluation Failed: {e}")
            return False

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
        
        print(f"DEBUG: Raw Variable {var_name} ({var_type}) = {var_value}")
    
        # Ensure var_value is not the type name ("int") by mistake
        if var_type == "int":
            try:
                var_value = int(var_value)  # Convert the value to an integer
            except ValueError:
                raise SyntaxError(f"Invalid integer value for variable {var_name}: {var_value}")
    
        # Store the actual value in the variable storage
        self.variables[var_name] = var_value
    
        print(f"DEBUG: Variable {var_name} = {self.variables[var_name]}")

    def execute_put(self):
        value = self.parser.parse_put()
        if value in self.variables:
            print(self.variables[value])  # Ensure variable values are printed
            return self.variables[value]  # Optional, useful for debugging
        else:
            print(f"DEBUG: Output {value}")

    def execute_if(self):
        """Executes an if statement by evaluating the condition."""
        condition_tokens = self.parser.parse_if_statement()

        # Convert condition tokens to a string
        condition_str = " ".join(token.value for token in condition_tokens)

        print(f"DEBUG: Evaluating Condition: {condition_str}")  # Debugging

        # Evaluate the condition
        condition_result = self.evaluate_condition(condition_str)

        print(f"DEBUG: Condition Evaluated To: {condition_result}")  # Debugging

        if condition_result:
            if self.parser.current_token.value == "{":  # ✅ Access parser's token
                self.parser.eat(TokenType.SYMBOL)  # Eat '{'
                while self.parser.current_token is not None and self.parser.current_token.value != "}":
                    self.execute_statement()
                self.parser.eat(TokenType.SYMBOL)  # Eat '}'
            else:
                self.execute_statement()
        else:
            print("DEBUG: Skipping if block because condition is False.")



source_code = """
import {arguments};


put{"Hello World"};
put{"Test code"};


var x int = 45;
var y int = 54;
put {x};
put {y};  
if ("x" > 10) {
    put {"SOME TIME"};
}
"""
    
lexer = Lexer(source_code)
tokens = lexer.tokenize()

parser = Parser(tokens)
parser.parse()
interpreter = Interpreter(parser)
interpreter.interpret()