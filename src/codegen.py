import json
from src.ast import *

# JSON generation helpers
def generate_action(action_id, text, action_type="0"):
    return {
        "id": str(action_id),
        "text": text,
        "t": action_type
    }

def generate_event(event_id, event_text, actions):
    return {
        "id": str(event_id),
        "text": event_text,
        "actions": actions
    }

def generate_content_block(events, alias="Script", class_name="script", global_id="\\b"):
    return {
        "content": events,
        "alias": alias,
        "class": class_name,
        "globalid": global_id
    }

# Codegen functions
def generate_variable_assignment(statement, action_id):
    text = [
        "Set variable",
        {"value": statement.variable_name, "l": "variable", "t": "string"},
        "to",
        {"value": str(statement.expression), "l": "any", "t": "string"}
    ]
    return generate_action(action_id, text)

def translate_statements(statements):
    actions = []
    action_id = 0

    for statement in statements:
        if isinstance(statement, VariableAssignment):
            action = generate_variable_assignment(statement, action_id)
            actions.append(action)
            action_id += 1
        elif isinstance(statement, ConsoleLog):
            action = generate_action(action_id, [
                "Log",
                {"value": str(statement.message.value if hasattr(statement.message, 'value') else statement.message).strip('"'), "t": "string"}
            ])
            actions.append(action)
            action_id += 1
        elif isinstance(statement, FunctionCall):
            action = generate_action(action_id, [
                "Run function",
                {"value": statement.function_name, "l": "function", "t": "string"}
            ])
            actions.append(action)
            action_id += 1
        elif isinstance(statement, IfStatement):
            operator_map = {
                "TokenType.EQUALS": "is equal to",
                "TokenType.NOT_EQUAL": "is not equal to",
                "TokenType.GREATER_THAN": "is greater than",
                "TokenType.LESS_THAN": "is less than"
            }
            op_str = operator_map.get(str(statement.operator), "is equal to")

            action = generate_action(action_id, [
                "If",
                {"value": str(statement.condition_left), "l": "any", "t": "string"},
                op_str,
                {"value": str(statement.condition_right), "l": "any", "t": "string"}
            ])
            actions.append(action)
            action_id += 1

            # Append body actions
            body_actions = translate_statements(statement.body)
            for ba in body_actions:
                ba['id'] = str(action_id)
                actions.append(ba)
                action_id += 1

            # Add end block
            actions.append(generate_action(action_id, ["end"]))
            action_id += 1

        elif isinstance(statement, RepeatForever):
            action = generate_action(action_id, [
                "Repeat forever"
            ])
            actions.append(action)
            action_id += 1

            # Append body actions
            body_actions = translate_statements(statement.body)
            for ba in body_actions:
                ba['id'] = str(action_id)
                actions.append(ba)
                action_id += 1

            # Add end block
            actions.append(generate_action(action_id, ["end"]))
            action_id += 1

        elif isinstance(statement, LogicWait):
            action = generate_action(action_id, [
                "Wait",
                {"value": str(statement.seconds), "t": "number"},
                "seconds"
            ])
            actions.append(action)
            action_id += 1

        elif isinstance(statement, LooksMake):
            # target should ideally check if it's string vs object id
            # for format.json it expects {"value": "D", "t": "object"}
            target_val = str(statement.target).strip('"')
            action = generate_action(action_id, [
                "Make",
                {"value": target_val, "t": "object"},
                statement.action
            ])
            actions.append(action)
            action_id += 1

        elif isinstance(statement, GetLocalUserId):
            action = generate_action(action_id, [
                "Get local user ID →",
                {"value": str(statement.target_variable).strip('"'), "l": "variable", "t": "string"}
            ])
            actions.append(action)
            action_id += 1

        elif isinstance(statement, NavigationRedirect):
            action = generate_action(action_id, [
                "Redirect to",
                {"value": str(statement.url).strip('"'), "t": "string", "href": "true"}
            ])
            actions.append(action)
            action_id += 1

        elif isinstance(statement, CreateTable):
            action = generate_action(action_id, [
                "Create table",
                {"value": str(statement.table_name).strip('"'), "l": "variable", "t": "string"}
            ])
            actions.append(action)
            action_id += 1

        elif isinstance(statement, GetCookie):
            action = generate_action(action_id, [
                "Get cookie",
                {"value": str(statement.cookie_name).strip('"'), "l": "cookie", "t": "string"},
                "→",
                {"value": str(statement.target_variable).strip('"'), "l": "variable", "t": "string"}
            ])
            actions.append(action)
            action_id += 1

        elif isinstance(statement, SplitString):
            action = generate_action(action_id, [
                "Split string",
                {"value": str(statement.source_string).strip('"'), "t": "string"},
                {"value": str(statement.separator).strip('"'), "l": "separator", "t": "string"},
                "→",
                {"value": str(statement.target_table).strip('"'), "l": "table", "t": "string"}
            ])
            actions.append(action)
            action_id += 1

        elif isinstance(statement, GetEntry):
            action = generate_action(action_id, [
                "Get entry",
                {"value": str(statement.index).strip('"'), "l": "entry", "t": "string"},
                "of",
                {"value": str(statement.table_name).strip('"'), "l": "table", "t": "string"},
                "→",
                {"value": str(statement.target_variable).strip('"'), "l": "variable", "t": "string"}
            ])
            actions.append(action)
            action_id += 1

        elif isinstance(statement, MathRound):
            action = generate_action(action_id, [
                "Round",
                {"value": str(statement.value).strip('"'), "l": "number", "t": "string"},
                "→",
                {"value": str(statement.target_variable).strip('"'), "l": "variable", "t": "string"}
            ])
            actions.append(action)
            action_id += 1

        else:
            continue

    return actions

def codegen(program):
    events = []
    event_id = 0

    for statement in program.statements:
        if isinstance(statement, Event):
            # For simplicity, map "WhenWebsiteLoaded" to "When website loaded..."
            # Later we can use a dictionary for mapping event names to UI texts
            event_name_text = "When website loaded..." if statement.event_name == "WhenWebsiteLoaded" else f"When {statement.event_name}..."
            event_text = [event_name_text]
            actions = translate_statements(statement.body)
            event = generate_event(event_id, event_text, actions)
            events.append(event)
            event_id += 1

    json_output = generate_content_block(events)

    json_string = json.dumps(json_output, indent=4)

    return json_string
