from src.lexer import *

if __name__ == '__main__':
    test_code = open("./examples/bugs.luax", "r").read()
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    # lexer.validate_semicolons()
    for token in tokens:
        print(token)