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
                "sequence": [TokenType.IDENTIFIER, TokenType.LPAREN],
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
            },
            {
                "sequence": [TokenType.IF],
                "callback": self._parse_if_statement
            },
            {
                "sequence": [TokenType.REPEAT_FOREVER],
                "callback": self._parse_repeat_forever
            },
            {
                "sequence": [TokenType.LOGIC_WAIT],
                "callback": self._parse_logic_wait
            },
            {
                "sequence": [TokenType.NAVIGATION_REDIRECT],
                "callback": self._parse_navigation_redirect
            },
            {
                "sequence": [TokenType.LOOKS_SHOW],
                "callback": lambda: self._parse_looks_make("visible")
            },
            {
                "sequence": [TokenType.LOOKS_HIDE],
                "callback": lambda: self._parse_looks_make("invisible")
            },
            {
                "sequence": [TokenType.NETWORK_GET_USERID],
                "callback": self._parse_get_local_user_id
            },
            {
                "sequence": [TokenType.TABLES_NEW],
                "callback": self._parse_create_table
            },
            {
                "sequence": [TokenType.COOKIES_GET_COOKIE],
                "callback": self._parse_get_cookie
            },
            {
                "sequence": [TokenType.STRINGS_SPLIT],
                "callback": self._parse_split_string
            },
            {
                "sequence": [TokenType.TABLES_GET_ENTRY],
                "callback": self._parse_get_entry
            },
            {
                "sequence": [TokenType.MATH_ROUND],
                "callback": self._parse_math_round
            }
        ]

        for pattern in patterns:
            offset = 0
            match = True
            for col in pattern["sequence"]:
                if self._is_at_end():
                    match = False
                    break
                token = self._peek(offset).type
                offset += 1
                if token != col:
                    match = False
                    break
            if match:
                return pattern["callback"]()

        raise SyntaxError(f"Unexpected token in parse_statement: {self._peek()}")

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
        body = []
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            body.append(self._parse_statement())
        self._consume(TokenType.RBRACE)
        return Event(event_name, arguments, body)

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

    def _parse_if_statement(self):
        self._consume(TokenType.IF)
        self._consume(TokenType.LPAREN)
        left = self._parse_expression()

        # operator like ==, !=, >, <
        token = self._peek()
        if token.type in [TokenType.EQUALS, TokenType.NOT_EQUAL, TokenType.GREATER_THAN, TokenType.LESS_THAN]:
            operator = self._consume(token.type).type
        else:
            raise SyntaxError(f"Expected comparison operator, found {token.type}")

        right = self._parse_expression()
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.LBRACE)
        body = []
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            body.append(self._parse_statement())
        self._consume(TokenType.RBRACE)
        return IfStatement(left, operator, right, body)

    def _parse_repeat_forever(self):
        self._consume(TokenType.REPEAT_FOREVER)
        self._consume(TokenType.LPAREN)
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.LBRACE)
        body = []
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            body.append(self._parse_statement())
        self._consume(TokenType.RBRACE)
        return RepeatForever(body)

    def _parse_logic_wait(self):
        self._consume(TokenType.LOGIC_WAIT)
        self._consume(TokenType.LPAREN)
        seconds = self._parse_expression()
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)
        return LogicWait(seconds)

    def _parse_navigation_redirect(self):
        self._consume(TokenType.NAVIGATION_REDIRECT)
        self._consume(TokenType.LPAREN)
        url = self._parse_expression()
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)
        return NavigationRedirect(url)

    def _parse_looks_make(self, action):
        if action == "visible":
            self._consume(TokenType.LOOKS_SHOW)
        else:
            self._consume(TokenType.LOOKS_HIDE)

        self._consume(TokenType.LPAREN)
        target = self._parse_expression()
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)
        return LooksMake(target, action)

    def _parse_get_local_user_id(self):
        self._consume(TokenType.NETWORK_GET_USERID)
        self._consume(TokenType.LPAREN)
        # Assuming the syntax implies passing the target variable name as an argument
        target_var = self._consume(TokenType.STRING).value
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)
        return GetLocalUserId(target_var)

    def _parse_create_table(self):
        self._consume(TokenType.TABLES_NEW)
        self._consume(TokenType.LPAREN)
        table_name = self._parse_expression()
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)
        return CreateTable(table_name)

    def _parse_get_cookie(self):
        self._consume(TokenType.COOKIES_GET_COOKIE)
        self._consume(TokenType.LPAREN)
        cookie_name = self._parse_expression()
        self._consume(TokenType.COMMA)
        target_variable = self._parse_expression()
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)
        return GetCookie(cookie_name, target_variable)

    def _parse_split_string(self):
        self._consume(TokenType.STRINGS_SPLIT)
        self._consume(TokenType.LPAREN)
        source = self._parse_expression()
        self._consume(TokenType.COMMA)
        separator = self._parse_expression()
        self._consume(TokenType.COMMA)
        target = self._parse_expression()
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)
        return SplitString(source, separator, target)

    def _parse_get_entry(self):
        self._consume(TokenType.TABLES_GET_ENTRY)
        self._consume(TokenType.LPAREN)
        index = self._parse_expression()
        self._consume(TokenType.COMMA)
        table = self._parse_expression()
        self._consume(TokenType.COMMA)
        target = self._parse_expression()
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)
        return GetEntry(index, table, target)

    def _parse_math_round(self):
        self._consume(TokenType.MATH_ROUND)
        self._consume(TokenType.LPAREN)
        value = self._parse_expression()
        self._consume(TokenType.COMMA)
        target = self._parse_expression()
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.SEMICOLON)
        return MathRound(value, target)

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
        return self._peek().type == TokenType.EOF

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
