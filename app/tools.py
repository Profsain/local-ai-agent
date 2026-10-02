from datetime import datetime
import ast, operator

_ALLOWED = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
            ast.Div: operator.truediv, ast.Mod: operator.mod, ast.Pow: operator.pow,
            ast.USub: operator.neg}

def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.operand))
    raise ValueError("Only basic arithmetic is allowed")

def calculator(expression: str):
    try:
        return str(_eval(ast.parse(expression[:100], mode="eval").body))
    except Exception as e:
        return f"Calculator error: {e}"

def current_time():
    return datetime.now().astimezone().isoformat()

TOOLS = {"calculator": calculator, "current_time": current_time}
TOOL_DEFINITIONS = [
    {"type":"function","function":{"name":"calculator","description":"Evaluate basic arithmetic.","parameters":{"type":"object","properties":{"expression":{"type":"string"}},"required":["expression"]}}},
    {"type":"function","function":{"name":"current_time","description":"Get the current local date and time.","parameters":{"type":"object","properties":{}}}},
]
