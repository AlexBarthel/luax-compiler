from src.lexer import *
from src.parser import *
from src.ast import *
from src.codegen import *

print("Tokenizing bugs.luau...")
lexer = Lexer(open("./examples/bugs.luax").read())
tokens = lexer.tokenize()


print("Parsing tokens...")
parser = Parser(tokens)
ast = parser.parse()

print("Generating code...")
program = Program(ast.statements)
json_output = codegen(program)

print(json_output)