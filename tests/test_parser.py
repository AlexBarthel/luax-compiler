from src.lexer import *
from src.parser import *

source_code = '''
@event WhenWebsiteLoaded() {
    if (x == y) {
        Console:Log("x equals y");
    }
    repeat_forever() {
        Logic:Wait(1);
    }
    Looks:Hide("D");
    Network:GetUserId("uid");
}
'''

lexer = Lexer(source_code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

print(ast.statements)
