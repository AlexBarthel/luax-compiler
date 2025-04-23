from src.lexer import *
from src.parser import *

source_code = '''
x = 5;
y = 10;
x = y;
-- Console.Log("Hello, World!");
'''

lexer = Lexer(source_code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

print(ast.statements)