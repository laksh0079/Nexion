OPERATORS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLICATION",
    "/": "DIVISION",
    ">": "GREATER",
    ">=": "GREATER_EQUAL",
    "<": "LESS",
    "<=": "LESS_EQUAL",
    "==": "EQUAL",
    "!=": "NOT_EQUAL",
    "=": "ASSIGN",
    "%": "MODULO"
}
PRECEDENCE = {
    "or": 70,
    "and": 75,
    "not": 80,
    "==": 85,
    "!=": 85,
    ">": 90,
    ">=": 90,
    "<": 90,
    "<=": 90,
    "+": 95,
    "-": 95,
    "*": 100,
    "/": 100,
    "%": 100
}

BINARY_OPERATORS = {"PLUS", "MINUS", "MULTIPLICATION", "DIVISION", "LESS", "GREATER", "LESS_EQUAL", "GREATER_EQUAL", "EQUAL", "NOT_EQUAL", "AND", "OR", "MODULO"}

OPERATOR_BEHAVIOUR = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
    "%": lambda a, b: a % b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    "and": lambda left, right: left and right,
    "or": lambda left, right: left or right
}

UNARY_BEHAVIOUR = {
    "not": lambda operand: not operand,
    "minus": lambda operand: -operand
}

OPERATOR_STARTS = {"+","-","*","/",">","<","!","=","%"}