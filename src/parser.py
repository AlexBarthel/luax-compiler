from src.lexer import *
from src.ast import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_position = 0

    def parse(self):
        statements = []
        while not self._is_at_end():
            statements.append(self._parse_statement())
        return Program(statements)

    def _parse_statement(self):
        token = self._peek()
        patterns = [
            {
                "sequence": [TokenType.IDENTIFIER, TokenType.ASSIGN],
                "callback": self._parse_variable_assignment
            },
            {
                "sequence": [TokenType.IDENTIFIER, TokenType.LPAREN, TokenType.RPAREN, TokenType.SEMICOLON],
                "callback": self._parse_function_call
            },
            {
                "sequence": [TokenType.EVENT],
                "callback": self._parse_event
            },
            {
                "sequence": [TokenType.FUNCTION],
                "callback": self._parse_function
            },
            {
                "sequence": [TokenType.CONSOLE_LOG],
                "callback": self._parse_console_log
            }
        ]

        for pattern in patterns:
            offset = 0
            for col in pattern["sequence"]:
                token = self._peek(offset).type
                # print(token)
                offset += 1
                if token == col: return pattern["callback"]()
                if token != col: break
        
        return Empty()

    def _parse_console_log(self):
        self._consume(TokenType.CONSOLE_LOG)
        self._consume(TokenType.LPAREN)
        message = self._consume(TokenType.STRING)
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)
        return ConsoleLog(message)

    def _parse_event(self):
        event_name = self._consume(TokenType.EVENT).value
        self._consume(TokenType.LPAREN)
        arguments = []
        if not self._check(TokenType.RPAREN):
            arguments.append(self._parse_expression())
            while self._check(TokenType.COMMA):
                self._consume(TokenType.COMMA)
                arguments.append(self._parse_expression())
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.LBRACE)
        return Event(event_name, arguments)
    
    def _parse_function(self):
        function_name = self._consume(TokenType.FUNCTION).value
        self._consume(TokenType.LPAREN)
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.LBRACE)
        return Function(function_name)
        pass

    def _parse_function_call(self):
        function_name = self._consume(TokenType.IDENTIFIER)
        self._consume(TokenType.LPAREN)
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)
        return FunctionCall(function_name)

    def _parse_variable_assignment(self):
        variable_name = self._consume(TokenType.IDENTIFIER).value
        self._consume(TokenType.ASSIGN)
        expression = self._parse_expression()
        self._consume(TokenType.SEMICOLON)
        return VariableAssignment(variable_name, expression)

    def _parse_expression(self):
        # Simple parsing for now; more complex expressions would require precedence parsing
        if self._check(TokenType.NUMBER):
            return self._consume(TokenType.NUMBER).value
        elif self._check(TokenType.STRING):
            return self._consume(TokenType.STRING).value
        elif self._check(TokenType.OBJECT_IDENTIFIER):
            return self._consume(TokenType.OBJECT_IDENTIFIER).value
        elif self._check(TokenType.IDENTIFIER):
            return self._consume(TokenType.IDENTIFIER).value
        else:
            raise SyntaxError(f"Unexpected token: {self._peek().type}")

    def _is_at_end(self):
        return self._peek(1).type == TokenType.EOF

    def _peek(self, offset=0):
        return self.tokens[self.current_position + offset]

    def _consume(self, expected_type):
        token = self._peek()
        if token.type == expected_type:
            self.current_position += 1
            return token
        raise SyntaxError(f"Expected {expected_type}, found {token.type}")

    def _check(self, token_type):
        return not self._is_at_end() and self._peek().type == token_type

    def _match(self, token_type):
        if self._check(token_type):
            self.current_position += 1
            return True
        return False
