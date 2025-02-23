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
