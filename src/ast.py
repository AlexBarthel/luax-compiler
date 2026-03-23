class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class Expression(ASTNode):
    pass

class Statement(ASTNode):
    pass

class VariableAssignment(Statement):
    def __init__(self, variable_name, expression):
        self.variable_name = variable_name
        self.expression = expression

class Event(Statement):
    def __init__(self, event_name, arguments, body):
        self.event_name = event_name
        self.arguments = arguments
        self.body = body

class Function(Statement):
    def __init__(self, function_name, body):
        self.function_name = function_name
        self.body = body

class FunctionCall(Statement):
    def __init__(self, function_name, arguments=None):
        self.function_name = function_name
        self.arguments = arguments if arguments is not None else []

class ConsoleLog(Statement):
    def __init__(self, message):
        self.message = message

class Empty():
    def __init__(self):
        pass

class IfThenElse(Statement):
    def __init__(self, condition_left, operator, condition_right, then_body, else_body=None):
        self.condition_left = condition_left
        self.operator = operator
        self.condition_right = condition_right
        self.then_body = then_body
        self.else_body = else_body if else_body is not None else []

class BinaryOperation(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        from src.lexer import TokenType
        operator_map = {
            TokenType.PLUS: "+",
            TokenType.MINUS: "-",
            TokenType.MULTIPLY: "*",
            TokenType.DIVIDE: "/",
            TokenType.MODULO: "%",
            TokenType.CONCAT: "::"
        }
        op_str = operator_map.get(self.operator, "+")
        # Ensure we stringify nested ones too
        return f"{self.left} {op_str} {self.right}"

class DefStatement(Statement):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

class IfStatement(Statement):
    def __init__(self, condition_left, operator, condition_right, body):
        self.condition_left = condition_left
        self.operator = operator
        self.condition_right = condition_right
        self.body = body

class RepeatForever(Statement):
    def __init__(self, body):
        self.body = body

class LogicWait(Statement):
    def __init__(self, seconds):
        self.seconds = seconds

class NavigationRedirect(Statement):
    def __init__(self, url):
        self.url = url

class LooksMake(Statement):
    def __init__(self, target, action):
        # action is "visible" or "invisible"
        self.target = target
        self.action = action

class GetLocalUserId(Statement):
    def __init__(self, target_variable):
        self.target_variable = target_variable

class CreateTable(Statement):
    def __init__(self, table_name):
        self.table_name = table_name

class GetCookie(Statement):
    def __init__(self, cookie_name, target_variable):
        self.cookie_name = cookie_name
        self.target_variable = target_variable

class SplitString(Statement):
    def __init__(self, source_string, separator, target_table):
        self.source_string = source_string
        self.separator = separator
        self.target_table = target_table

class GetEntry(Statement):
    def __init__(self, index, table_name, target_variable):
        self.index = index
        self.table_name = table_name
        self.target_variable = target_variable

class MathRound(Statement):
    def __init__(self, value, target_variable):
        self.value = value
        self.target_variable = target_variable