from src.ast import *
from src.codegen import *
from src.lexer import TokenType

statements = [
    Event("WhenWebsiteLoaded", [], [
        VariableAssignment("x", 5),
        VariableAssignment("y", 10),
        VariableAssignment("x", "y"),
        ConsoleLog("Hello, World!"),
        FunctionCall("verify_request", []),
        IfStatement("x", TokenType.EQUALS, "y", [
            ConsoleLog("x equals y")
        ]),
        RepeatForever([
            LogicWait(1)
        ]),
        LooksMake('"D"', "visible"),
        LooksMake('"@"', "invisible"),
        GetLocalUserId('"uid"'),
        NavigationRedirect('"bloxchain.rbx"'),
        CreateTable('"queue"'),
        GetCookie('"req"', '"req"'),
        SplitString('"{req}"', '","', '"headers"'),
        GetEntry('"1"', '"headers"', '"_id"'),
        MathRound('"5.5"', '"r"')
    ])
]

program = Program(statements)
json_output = codegen(program)

print(json_output)
