import sys
from sly import Lexer, Parser

class unicodingLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { COMMAND, INT, FLOAT, COMMA, LBRACE, RBRACE, COLON, STRING, IDENTIFIER}
    # String containing ignored characters between tokens
    ignore = ' \t'
    ignore_comment = r'\#.*'

    # Regular expression rules for tokens
    COMMAND = r'\([a-zA-Z_][a-zA-Z0-9_]*\)'
    INT     = r'\d+'
    FLOAT   = r'\d+\.\d+'
    LBRACE  = r'\{'
    RBRACE  = r'\}'
    COLON   = r'\:'
    COMMA   = r'\,'
    STRING  = r'\".*?\"'
    IDENTIFIER  = r'[a-zA-Z_][]a-zA-Z0-9_]*'

class unicodingParser(Parser):
    tokens = unicodingLexer.tokens

    def error(self, p):
        if p != None:
            if p:
                print(f"Error {p.type, p.value}")
            else:
                print("Error")


    @_('COMMAND COLON block')
    def statement(self, p):
        return ('command', p.COMMAND, p.block)
    
    @_('LBRACE args RBRACE')
    def block(self, p):
        return p.args
    
    @_('args COMMA arg')
    def args(self, p):
        return p.args + [p.arg]
        
    @_('arg')
    def args(self, p):
        return [p.arg]
    
    @_('STRING')
    def arg(self, p):
        return p.STRING[1:-1]
        
    @_('INT')
    def arg(self, p):
        return int(p.INT)
        
    @_('FLOAT')
    def arg(self, p):
        return float(p.FLOAT)
    
    @_('IDENTIFIER')
    def arg(self, p):
        return p.IDENTIFIER
    
def interpretator(ast):
    commands = ["(print)", "(var)"]
    if ast is not None and ast[1] in commands:
        command, name, content = ast
        cmd_name = name[1:-1]
    
        if cmd_name == 'print':
            print(*content)
        if cmd_name == 'var':
            eval(*content)
            
def shell_mode():
    lexer = unicodingLexer()
    parser = unicodingParser()
    while True:
        data = input(">>> ")
    
        if data == "(exit)":
            break
        ast = parser.parse(lexer.tokenize(data))
        interpretator(ast)

def script_mode():
    lexer = unicodingLexer()
    parser = unicodingParser()
    if len(sys.argv) > 2:
        num_line = 0
        with open(sys.argv[2], 'r') as f:
            for line in f:
                num_line += 1
                try:
                    ast = parser.parse(lexer.tokenize(line.rstrip('\n')))
                    interpretator(ast)
                except Exception as e:
                    print(f"Error in {num_line} line: {e}")
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "shell":
            shell_mode()
        if sys.argv[1] == "run":
            script_mode()
    
