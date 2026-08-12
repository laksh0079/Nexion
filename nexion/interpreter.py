from AST.program import Program
from AST.statements import SetStatement, SayStatement
from AST.expressions import StringLiteral, NumberLiteral, Identifier, BinaryExpression, BooleanLiteral, UnaryExpression
from operators import OPERATOR_BEHAVIOUR, UNARY_BEHAVIOUR
class Interpreter:
    def __init__(self, root):
        self.root = root
        self.variables={}
        
    def apply_operator(self, left, mid, right):
        if mid in ["+","-","*","/"]:
            if type(left) is bool or type(right) is bool:
                raise Exception("Type Error: Cannot use Boolean in Arithmetic")
        if mid in OPERATOR_BEHAVIOUR:
            return OPERATOR_BEHAVIOUR[mid](left, right)
        raise Exception("Unknown operator", mid)
    def apply_unary(self, operator, operand):
        if operator in UNARY_BEHAVIOUR.keys():
            return UNARY_BEHAVIOUR[operator](operand)
        raise Exception("Unknknown operator", operator)
    def execute(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.execute(statement)
        elif isinstance(node, SetStatement):
            name = node.variable.name
            value = self.evaluate(node.value)
            self.variables[name] = value
        elif isinstance(node, SayStatement):
            print(self.evaluate(node.value))
    def evaluate(self, node):
        if isinstance(node, StringLiteral):
            return node.string
        elif isinstance(node, NumberLiteral):
            return node.number
        elif isinstance(node, Identifier):
            if node.name in self.variables:
                return self.variables[node.name]
            else:
                raise Exception(f"The variable {node.name} does not exist")
        elif isinstance(node, BinaryExpression):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            print("EVAL:", left, node.root, right)
            return self.apply_operator(left, node.root, right)
        elif isinstance(node, BooleanLiteral):
            return node.value
        elif isinstance(node, UnaryExpression):
            operand = self.evaluate(node.operand)
            return self.apply_unary(node.operator, operand)
    def run(self):
        self.execute(self.root) 
        