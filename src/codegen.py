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

def generate_event_definition(statement, action_id):
    text = [
        "Run event",
        {"value": statement.event_name, "l": "function", "t": "string"}
    ]
    # Add arguments if needed
    return generate_action(action_id, text)

def translate_statements(statements):
    actions = []
    action_id = 0

    for statement in statements:
        if isinstance(statement, VariableAssignment):
            action = generate_variable_assignment(statement, action_id)
        elif isinstance(statement, Event):
            action = generate_event_definition(statement, action_id)
        else:
            continue
        
        actions.append(action)
        action_id += 1

    return actions

def codegen(program):
    events = []
    event_id = 0
    
    event_text = ["When website loaded..."]
    actions = translate_statements(program.statements)
    
    event = generate_event(event_id, event_text, actions)
    events.append(event)
    
    json_output = generate_content_block(events)
    
    json_string = json.dumps(json_output, indent=4)
    
    return json_string
