from src.ast import *
from src.codegen import *

statements = [
    VariableAssignment("x", 5),
    VariableAssignment("y", 10),
    VariableAssignment("x", "y"),
    FunctionCall("Console.Log", ["Hello, World!"])
]

program = Program(statements)
json_output = codegen(program)

print(json_output)