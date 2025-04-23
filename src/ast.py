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
    def __init__(self, event_name, arguments):
        self.event_name = event_name
        self.arguments = arguments

class Function(Statement):
    def __init__(self, function_name):
        self.function_name = function_name

class FunctionCall(Statement):
    def __init__(self, function_name):
        self.function_name = function_name

class ConsoleLog(Statement):
    def __init__(self, message):
        self.message = message

class Empty():
    def __init__(self):
        pass