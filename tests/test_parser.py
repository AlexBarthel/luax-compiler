from src.lexer import *
from src.parser import *

source_code = '''
@event WhenWebsiteLoaded
    x = 5
    Console:Log "Hello world!"
'''

lexer = Lexer(source_code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

print(ast.statements)
