from error_handler import John, LongSyntaxError, VariableDeclarationError, ControlFlowException
from lexer import Lexer
from parser import Parser
from grammar_parser import Interpreter
import sys

class ContextManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.error_handler = John()
        
    def run(self):
        """Reads the file and executes Lexing -> Parsing -> Interpreting with error handling."""
        try:
            global source_code
            with open(self.file_path, 'r') as file:
                source_code = file.read()
                
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            
            parser = Parser(tokens)
            parser.parse()
            interpreter = Interpreter(parser)
            interpreter.interpret()
        except:
            pass
    
if __name__ == "__main__":
    # import sys
    
    # if len(sys.argv) != 2:
    #     print("Usage: python context_manager.py <file.rgr>")
    #     sys.exit(1)
    
    # file_path = sys.argv[1]
    
    manager = ContextManager("example.rgr")
    manager.run()
