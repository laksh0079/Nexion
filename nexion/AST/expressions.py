class Expressions:
    pass


class NoneLiteral:
    def __init__(self):
        self.value = None
    
class NumberLiteral(Expressions):
    def __init__(self, number):
        self.number = number
    def __repr__(self):
        return f"Number: {self.number}"

class FloatLiteral:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Float: {self.value}"

class StringLiteral(Expressions):
    def __init__(self, string):
        self.string = string
    def __repr__(self):
        return f"String: {self.string}"

class Identifier(Expressions):
    def __init__(self, name):
       self.name = name
    def __repr__(self):
        return f"Identifier: {self.name}"

class BinaryExpression(Expressions):
    def __init__(self, left, root, right):
        self.left = left
        self.root = root
        self.right = right
    def __repr__(self):
        return f"Left: {self.left}, Mid: {self.root}, Right: {self.right}"

class BooleanLiteral(Expressions):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Boolean: {self.value}"
class UnaryExpression(Expressions):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand
    def __repr__(self):
        return f"Unary: Operator: {self.operator}, Operand: {self.operand}"
        
class ListLiteral:
    def __init__(self, elements=[]):
        self.elements = elements
    def __repr__(self):
        return f"Elements: {self.elements}"

        
class IndexExpression:
    def __init__(self, target, index):
        self.target = target
        self.index = index
        
    def __repr__(self):
        return f"{self.target}[{self.index}]"
       
class IndexAssignment:
    def __init__(self, target, value):
        self.target = target
        self.value = value
    def __repr__(self):
        return f"{self.target} = {self.value}"
        
class DictLiteral:
    def __init__(self, entries=[]):
        self.entries = entries
    def __repr__(self):
        return f"Entries: {self.entries}"
    
class SliceExpression:
    def __init__(self, target, start=None, end=None):
        self.target = target
        self.start = start
        self.end = end
    def __repr__(self):
        return f"Target: {self.target}, start: {self.start}, end: {self.end}"