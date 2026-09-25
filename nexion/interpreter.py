from AST.program import Program
from AST.statements import LetStatement, AssignStatement, SayStatement, IfStatement, Block, Scope, WhileStatement, NextStatement, ExitStatement, Function, FunCall
from AST.exceptions import NextSignal, ExitSignal
from AST.expressions import StringLiteral, NumberLiteral, Identifier, BinaryExpression, BooleanLiteral, UnaryExpression
from operators import OPERATOR_BEHAVIOUR, UNARY_BEHAVIOUR
class Interpreter:
    def __init__(self, root):
        self.root = root
        self.global_scope = Scope({})
        self.current_scope = self.global_scope
        self.functions = {}
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
    
    def index_functions(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                if isinstance(statement, Function):
                    self.functions[statement.name] = statement
        
    def execute(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.execute(statement)
        elif isinstance(node, LetStatement):
            name = node.variable.name
            value = self.evaluate(node.value)
            self.current_scope.variables[name] = value
        elif isinstance(node, AssignStatement):
            name = node.variable.name
            lookup_scope = self.current_scope
            while lookup_scope is not None:
                if name in lookup_scope.variables:
                    lookup_scope.variables[name] = self.evaluate(node.value)
                    break
                else:
                    lookup_scope = lookup_scope.parent
            else:
                raise Exception(f"The variable {name} does not exist")
        elif isinstance(node, SayStatement):
            print(self.evaluate(node.value))
        elif isinstance(node, IfStatement):
            res = self.evaluate(node.condition)
            if type(res) is not bool:
                raise Exception(f"Runtime Error: If condition must be boolean, got {type(res).__name__}")
            if res:
                for statement in node.statements.statements:
                    self.execute(statement)
            else:
                if node.else_branch is not None:
                    if isinstance(node.else_branch, IfStatement):
                        self.execute(node.else_branch)
                    else:
                        for statement in node.else_branch.statements:
                            self.execute(statement)
        elif isinstance(node, Block):
            self.current_scope = Scope({}, self.current_scope)
            for statement in node.statements:
                self.execute(statement)
            self.current_scope = self.current_scope.parent
        elif isinstance(node, WhileStatement):
            while True:
                condition = self.evaluate(node.condition)
                if type(condition) is not bool:
                    raise Exception(f"Runtime Error: While condition must be boolean, got {type(res).__name__}")
                if condition:
                    try:
                        for statement in node.statements.statements:
                            self.execute(statement)
                    except ExitSignal:
                        break
                    except NextSignal:
                        continue
                else:
                    break
        elif isinstance(node, ExitStatement):
            raise ExitSignal()
        elif isinstance(node, NextStatement):
            raise NextSignal()
        elif isinstance(node, FunCall):
            if not node.name in self.functions:
                raise Exception(f"Runtime Error: The Function {node.name} Does Not Exist")
            #arguments = node.arguments
            var_list = {}
            func = self.functions[node.name]
            if len(func.parameters) != len(node.arguments):
                raise Exception("Runtime Error: The lengths of the given parameters and arguments do not match.")
            for p, a in zip(func.parameters, node.arguments):
                var_list[p.name] = self.evaluate(a)
            print(var_list)
            self.current_scope = Scope(var_list, self.current_scope)
            self.execute(func.statements)
            self.current_scope = self.current_scope.parent
    def evaluate(self, node):
        if isinstance(node, StringLiteral):
            return node.string
        elif isinstance(node, NumberLiteral):
            return node.number
        elif isinstance(node, Identifier):
            lookup_scope = self.current_scope
            while lookup_scope is not None:
                if node.name in lookup_scope.variables:
                    return lookup_scope.variables[node.name]
                else:
                    lookup_scope = lookup_scope.parent
            raise Exception(f"The variable {node.name} does not exist")
        elif isinstance(node, BinaryExpression):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            #print("EVAL:", left, node.root, right)
            return self.apply_operator(left, node.root, right)
        elif isinstance(node, BooleanLiteral):
            return node.value
        elif isinstance(node, UnaryExpression):
            operand = self.evaluate(node.operand)
            return self.apply_unary(node.operator, operand)
        
            
            
    def run(self):
        self.index_functions(self.root)
        try:
            self.execute(self.root) 
        except ExitSignal:
            raise Exception("Runtime Error: 'exit' used outside of a loop.")
        except NextSignal:
            raise Exception("Runtime Error: 'continue' used outside of a loop.")