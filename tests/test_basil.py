from src.lexer import *
from src.parser import *
from src.codegen import *

source_code = '''
def calculate =
    x = 5
    y = 10
    z = x + y

@event WhenWebsiteLoaded =
    if x == y then
        Console:Log "x equals y"
    else
        Console:Log "x != y"

    repeat_forever
        Logic:Wait 1

    calculate
    Looks:Hide "D"
    Network:GetUserId "uid"
'''

lexer = Lexer(source_code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
json_output = codegen(ast)

print(json_output)
