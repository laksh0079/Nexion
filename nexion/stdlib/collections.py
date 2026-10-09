from AST.exceptions import UnknownTypeError

def length(value):
    return len(value)
    
def get_type(value):
    types = {
            int: "int",
            str: "string",
            bool: "boolean",
            type(None): "none",
            list: "list",
            dict: "dict"
        }
    try:
        return types[type(value)]
    except KeyError:
        raise UnknownTypeError(f"Runtime Error: Unknown Data Type: {type(value).__name__}")
        
def to_string(value, indent=0):
    if value is True:
        value = "true"
    elif value is False:
        value = "false"
    elif value is None:
        value = "none"
    elif isinstance(value, list):
        string = "["
        for v in value:
            if string != "[":
                string += ", "
            if isinstance(v, str):
                string += f'"{to_string(v)}"'
            else:
                string += to_string(v)
        string += "]"
        value = string
    elif isinstance(value, dict):
        string = "{"
        length = len(value.items())
        indent += 1
        spaces = " " * 4 * indent
        temp= " " * 4 * (indent - 1)
        for i, (k, v) in enumerate(value.items()):
            if i == 0:
                string += "\n"
            if isinstance(k, str) and isinstance(v, str):
                string += f'{spaces}"{to_string(k)}": "{to_string(v)}"'
            elif isinstance(k, str):
                string += f'{spaces}"{to_string(k)}": {to_string(v, indent)}'
            elif isinstance(v, str):
                string += f'{spaces}{to_string(k)}: "{to_string(v)}"'
            else:
                string += f"{spaces}{to_string(k)}: {to_string(v, indent)}"
            if i != length - 1:
                string += ",\n"
            elif i == length - 1:
                string+="\n"
        string += f"{temp}}}"
        value = string
    else:
        value = str(value)
    return value