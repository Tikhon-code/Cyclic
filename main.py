from sly import Lexer, Parser

class shLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { COMMAND, NUMBER, COMMA, LBRACE, RBRACE, COLON, STRING, IDENTIFIER, NONE}
    literals = {'=', '+', '-', '*', '/', '(', ')', '{', '}', ':', ',', '|'}
    # String containing ignored characters between tokens
    ignore = ' \t'

    # Regular expression rules for tokens
    COMMAND = r'\([a-zA-Z_][a-zA-Z0-9_]*\)'
    NUMBER  = r'\d+'
    LBRACE  = r'\{'
    RBRACE  = r'\}'
    COLON   = r':'
    COMMA   = r','
    STRING  = r'\".*?\"'
    IDENTIFIER  = r'[a-zA-Z_][]a-zA-Z0-9_]*'
    
class shParser(Parser):
    tokens = shLexer.tokens

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
        
    @_('NUMBER')
    def arg(self, p):
        return int(p.NUMBER)
        
    @_('IDENTIFIER')
    def arg(self, p):
        return p.IDENTIFIER
    
def interpretator(ast):
    commands = ["(print)"]
    if ast is not None and ast[1] in commands:
        command, name, content = ast
        cmd_name = name[1:-1]
    
        if cmd_name == 'print':
            print(*content)
        else:
            print(f"{ast[1]} is not system command")
    else:
        print("Err")
if __name__ == '__main__':
    lexer = shLexer()
    parser = shParser()
    while True:
        data = input(">>> ")
    
        ast = parser.parse(lexer.tokenize(data))
        interpretator(ast)
