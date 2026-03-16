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

        if token.type == TokenType.EVENT:
            return self._parse_event()
        if token.type == TokenType.DEF:
            return self._parse_def()
        if token.type == TokenType.IF:
            return self._parse_if_statement()
        if token.type == TokenType.REPEAT_FOREVER:
            return self._parse_repeat_forever()

        # Action/Functions that stand on their own
        if token.type == TokenType.CONSOLE_LOG:
            self._consume(TokenType.CONSOLE_LOG)
            message = self._parse_expression()
            return ConsoleLog(message)
        if token.type == TokenType.LOGIC_WAIT:
            self._consume(TokenType.LOGIC_WAIT)
            seconds = self._parse_expression()
            return LogicWait(seconds)
        if token.type == TokenType.NAVIGATION_REDIRECT:
            self._consume(TokenType.NAVIGATION_REDIRECT)
            url = self._parse_expression()
            return NavigationRedirect(url)
        if token.type == TokenType.LOOKS_SHOW:
            self._consume(TokenType.LOOKS_SHOW)
            target = self._parse_expression()
            return LooksMake(target, "visible")
        if token.type == TokenType.LOOKS_HIDE:
            self._consume(TokenType.LOOKS_HIDE)
            target = self._parse_expression()
            return LooksMake(target, "invisible")
        if token.type == TokenType.NETWORK_GET_USERID:
            self._consume(TokenType.NETWORK_GET_USERID)
            target_var = self._parse_expression()
            return GetLocalUserId(target_var)
        if token.type == TokenType.TABLES_NEW:
            self._consume(TokenType.TABLES_NEW)
            table_name = self._parse_expression()
            return CreateTable(table_name)
        if token.type == TokenType.COOKIES_GET_COOKIE:
            self._consume(TokenType.COOKIES_GET_COOKIE)
            cookie_name = self._parse_expression()
            target_variable = self._parse_expression()
            return GetCookie(cookie_name, target_variable)
        if token.type == TokenType.STRINGS_SPLIT:
            self._consume(TokenType.STRINGS_SPLIT)
            source = self._parse_expression()
            separator = self._parse_expression()
            target = self._parse_expression()
            return SplitString(source, separator, target)
        if token.type == TokenType.TABLES_GET_ENTRY:
            self._consume(TokenType.TABLES_GET_ENTRY)
            index = self._parse_expression()
            table = self._parse_expression()
            target = self._parse_expression()
            return GetEntry(index, table, target)
        if token.type == TokenType.MATH_ROUND:
            self._consume(TokenType.MATH_ROUND)
            value = self._parse_expression()
            target = self._parse_expression()
            return MathRound(value, target)

        # We don't have newlines, so tracking the end of an expression vs assignment requires care
        # If it's an IDENTIFIER followed by ASSIGN it's an assignment
        if token.type == TokenType.IDENTIFIER and not self._is_at_end() and self.current_position + 1 < len(self.tokens) and self._peek(1).type == TokenType.ASSIGN:
            return self._parse_variable_assignment()

        # Try parsing an expression/function call
        # Since Basil is expression-based, a statement could just be an expression
        expr = self._parse_expression()

        # Since Basil functions can be called inline with space: e.g. `calculate arg1 arg2`
        # If expr is just an identifier or we have more arguments that look like expressions
        # But we don't want to turn numbers into function calls
        if isinstance(expr, str) and not expr.isdigit():
            # This could be an inline function call without parens
            args = []
            while not self._is_at_end() and self._peek().type not in [TokenType.EOF]:
                # check if next token is a keyword or starts a new assignment
                nxt = self._peek()
                if nxt.type in [TokenType.IF, TokenType.THEN, TokenType.ELSE, TokenType.DEF, TokenType.EVENT, TokenType.REPEAT_FOREVER, TokenType.CONSOLE_LOG, TokenType.LOGIC_WAIT, TokenType.NAVIGATION_REDIRECT, TokenType.LOOKS_SHOW, TokenType.LOOKS_HIDE, TokenType.NETWORK_GET_USERID, TokenType.TABLES_NEW, TokenType.COOKIES_GET_COOKIE, TokenType.STRINGS_SPLIT, TokenType.TABLES_GET_ENTRY, TokenType.MATH_ROUND]:
                    break
                if nxt.type == TokenType.IDENTIFIER:
                    if self.current_position + 1 < len(self.tokens) and self._peek(1).type == TokenType.ASSIGN:
                        break
                try:
                    # We just test parse primary. Since expressions could consume multiple things, we just look for single argument entities.
                    args.append(self._parse_primary())
                except SyntaxError:
                    break

            # Assume it's a function call if it's an identifier standalone as a statement.
            return FunctionCall(expr, args)

        return expr

    def _parse_def(self):
        self._consume(TokenType.DEF)
        name = self._consume(TokenType.IDENTIFIER).value
        params = []
        while self._peek().type == TokenType.IDENTIFIER:
            params.append(self._consume(TokenType.IDENTIFIER).value)
        if self._check(TokenType.ASSIGN):
            self._consume(TokenType.ASSIGN)
        body = self._parse_block()
        return DefStatement(name, params, body)

    def _parse_event(self):
        event_name = self._consume(TokenType.EVENT).value
        # @event name expr expr = body
        args = []
        while self._peek().type == TokenType.IDENTIFIER:
            args.append(self._consume(TokenType.IDENTIFIER).value)
        if self._check(TokenType.ASSIGN):
            self._consume(TokenType.ASSIGN)

        # Parse multiple statements inside an event block
        body = []
        while not self._is_at_end():
            if self._peek().type in [TokenType.EVENT, TokenType.DEF, TokenType.EOF]:
                break
            body.append(self._parse_statement())

        return Event(event_name, args, body)

    def _parse_variable_assignment(self):
        variable_name = self._consume(TokenType.IDENTIFIER).value
        self._consume(TokenType.ASSIGN)
        # Because we consume an expression without semicolons or line breaks,
        # we might accidentally consume more than the assignment's expression.
        # But our simple expression parser will stop when it finishes parsing binary ops.
        expression = self._parse_expression()
        return VariableAssignment(variable_name, expression)


    def _parse_if_statement(self):
        self._consume(TokenType.IF)
        left = self._parse_expression()

        token = self._peek()
        if token.type in [TokenType.EQUALS, TokenType.NOT_EQUAL, TokenType.GREATER_THAN, TokenType.LESS_THAN]:
            operator = self._consume(token.type).type
        else:
            raise SyntaxError(f"Expected comparison operator, found {token.type}")

        right = self._parse_expression()
        self._consume(TokenType.THEN)

        then_body = self._parse_block()
        else_body = []
        if self._check(TokenType.ELSE):
            self._consume(TokenType.ELSE)
            else_body = self._parse_block()

        return IfThenElse(left, operator, right, then_body, else_body)

    def _parse_repeat_forever(self):
        self._consume(TokenType.REPEAT_FOREVER)
        body = self._parse_block()
        return RepeatForever(body)

    def _parse_block(self):
        # We'll parse statements until we run into an EOF or a token that's not valid as a statement
        statements = []
        while not self._is_at_end():
            # In a real Basil language, newline and indentation matter.
            # We'll just try to parse a statement. If it fails, we break.
            if self._peek().type in [TokenType.ELSE, TokenType.EOF]:
                break
            if len(statements) > 0 and self._peek().type in [TokenType.DEF, TokenType.EVENT]:
                break
            stmt = self._parse_statement()
            statements.append(stmt)
        return statements

    def _parse_expression(self):
        return self._parse_binary(0)

    def _parse_binary(self, min_prec):
        left = self._parse_primary()

        precedences = {
            TokenType.PLUS: 10,
            TokenType.MINUS: 10,
            TokenType.MULTIPLY: 20,
            TokenType.DIVIDE: 20,
            TokenType.MODULO: 20,
            TokenType.CONCAT: 5
        }

        while True:
            token = self._peek()
            prec = precedences.get(token.type, -1)
            if prec < min_prec:
                break

            operator = self._consume(token.type).type
            right = self._parse_binary(prec + 1)
            left = BinaryOperation(left, operator, right)

        return left

    def _parse_primary(self):
        if self._check(TokenType.NUMBER):
            return self._consume(TokenType.NUMBER).value
        elif self._check(TokenType.STRING):
            return self._consume(TokenType.STRING).value
        elif self._check(TokenType.IDENTIFIER):
            return self._consume(TokenType.IDENTIFIER).value
        elif self._check(TokenType.LPAREN):
            self._consume(TokenType.LPAREN)
            expr = self._parse_expression()
            self._consume(TokenType.RPAREN)
            return expr
        else:
            raise SyntaxError(f"Unexpected token in primary expression: {self._peek()}")

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
