from AST.program import Program
from AST.statements import LetStatement, AssignStatement, SayStatement, IfStatement, Block, Scope, WhileStatement, NextStatement, ExitStatement, Function, FunCall, ReturnStatement
from AST.exceptions import NextSignal, ExitSignal, ReturnSignal, UnknownTypeError
from AST.expressions import StringLiteral, NumberLiteral, Identifier, BinaryExpression, BooleanLiteral, UnaryExpression, NoneLiteral, ListLiteral, IndexExpression, IndexAssignment, DictLiteral
from operators import OPERATOR_BEHAVIOUR, UNARY_BEHAVIOUR
class Interpreter:
    def get_type(self, value):
        types = {
            int: "int",
            str: "string",
            bool: "boolean",
            type(None): "none",
            list: "list"
        }
        try:
            return types[type(value)]
        except KeyError:
            raise UnknownTypeError(f"Runtime Error: Unknown Data Type: {type(value).__name__}")
    def __init__(self, root):
        self.root = root
        self.global_scope = Scope({})
        self.current_scope = self.global_scope
        self.functions = {}
        self.MATH_OPERATORS = {"+", "-", "*", "/", "%"}
        
    def apply_operator(self, left, mid, right):
        if mid in ["+","-","*","/"]:
            if self.get_type(left) == "boolean" or self.get_type(right) == "boolean":
                raise Exception("Type Error: Cannot use Boolean in Arithmetic")
        if mid in OPERATOR_BEHAVIOUR:
            return OPERATOR_BEHAVIOUR[mid](left, right)
        raise Exception("Unknown operator", mid)
    def apply_unary(self, operator, operand):
        if operator in UNARY_BEHAVIOUR.keys():
            return UNARY_BEHAVIOUR[operator](operand)
        raise Exception("Unknknown operator", operator)
    
    def index_functions(self, node):
        if type(node) is Program:
            for statement in node.statements:
                if type(statement) is Function:
                    self.functions[statement.name] = statement
        
    def execute(self, node):
        if type(node) is Program:
            for statement in node.statements:
                self.execute(statement)
        elif type(node) is LetStatement:
            name = node.variable.name
            value = self.evaluate(node.value)
            self.current_scope.variables[name] = value
        elif type(node) is AssignStatement:
            name = node.variable.name.name
            lookup_scope = self.current_scope
            while lookup_scope is not None:
                if name in lookup_scope.variables:
                    lookup_scope.variables[name] = self.evaluate(node.value)
                    break
                else:
                    lookup_scope = lookup_scope.parent
            else:
                raise Exception(f"The variable {name} does not exist")
        elif type(node) is SayStatement:
            arg = self.evaluate(node.value)
            if (arg is None):
                print("none")
            else:
                print(arg)
        elif type(node) is IfStatement:
            res = self.evaluate(node.condition)
            if self.get_type(res) != "boolean":
                raise Exception(f"Runtime Error: If condition must be boolean, got {self.get_type(res)}")
            if res:
                
                self.execute(node.statements)
            else:
                if node.else_branch is not None:
                    if type(node.else_branch) is IfStatement:
                        self.execute(node.else_branch)
                    else:
                        self.execute(node.else_branch)
        elif type(node) is Block:
            previous_scope = self.current_scope
            self.current_scope = Scope({}, previous_scope)
            try:
                for statement in node.statements:
                    self.execute(statement)
            finally:  
                self.current_scope = previous_scope
        elif type(node) is WhileStatement:
            while True:
                condition = self.evaluate(node.condition)
                if not self.get_type(condition) == "boolean":
                    raise Exception(f"Runtime Error: While condition must be boolean, got {self.get_type(condition)}")
                if condition:
                    try:
                        self.execute(node.statements)
                    except ExitSignal:
                        break
                    except NextSignal:
                        continue
                else:
                    break
        elif type(node) is ExitStatement:
            raise ExitSignal()
        elif type(node) is NextStatement:
            raise NextSignal()
        elif type(node) is ReturnStatement:
            if node.value is None:
                raise ReturnSignal()
            return_val = self.evaluate(node.value)
            raise ReturnSignal(return_val)
        elif type(node) is FunCall:
            self.evaluate(node)
        elif type(node) is IndexAssignment:
            self.evaluate(node)
 
    def evaluate(self, node):
        if type(node) is StringLiteral:
            return node.string
        elif type(node) is NumberLiteral:
            return node.number
        elif type(node) is Identifier:
            lookup_scope = self.current_scope
            while lookup_scope is not None:
                if node.name in lookup_scope.variables:
                    return lookup_scope.variables[node.name]
                else:
                    lookup_scope = lookup_scope.parent
            raise Exception(f"The variable {node.name} does not exist")
        elif type(node) is BinaryExpression:
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.root in self.MATH_OPERATORS:
                if self.get_type(left) == "none" or self.get_type(right) == "none":
                    raise Exception("Runtime Error: Cannot Perform Mathematical operations on 'none'")
            #print("EVAL:", left, node.root, right)
            return self.apply_operator(left, node.root, right)
        elif type(node) is ListLiteral:
            return [self.evaluate(element) for element in node.elements]
        elif type(node) is BooleanLiteral:
            return node.value
        elif type(node) is UnaryExpression:
            operand = self.evaluate(node.operand)
            return self.apply_unary(node.operator, operand)
        elif type(node) is NoneLiteral:
            return node.value
        elif type(node) is DictLiteral:
            entries = {}
            for sublist in node.entries:
                entries[self.evaluate(sublist[0])] = self.evaluate(sublist[1])
            return entries
        elif isinstance(node, FunCall):
             if not node.name.name in self.functions:
                raise Exception(f"Runtime Error: The Function {node.name} Does Not Exist")
            #arguments = node.arguments
             var_list = {}
             func = self.functions[node.name.name]
             if len(func.parameters) != len(node.arguments):
                 raise Exception("Runtime Error: The lengths of the given parameters and arguments do not match.")
             for p, a in zip(func.parameters, node.arguments):
                 var_list[p.name] = self.evaluate(a)
             previous_scope = self.current_scope
             self.current_scope = Scope(var_list, previous_scope)

             try:
                 self.execute(func.statements)
             except ReturnSignal as r:
                 return r.value
             finally:
                 self.current_scope = previous_scope
        elif type(node) is IndexExpression:
            target = self.evaluate(node.target.target)
            index = self.evaluate(node.index)
            if not self.get_type(index) == "int":
                raise Exception("Runtime Error: Index Can Only Be Of Type Int")
            if not self.get_type(target) == "list":
                raise Exception("Runtime Error: Value is not Indexable")
            if 0 <= index < len(target):
                return target[index]
            else:
                raise Exception("Runtime Erorr: Index Out of Range")
        elif type(node) is IndexAssignment:
            target = self.evaluate(node.target.target)
            target[self.evaluate(node.target.index)] = self.evaluate(node.value)
            
    def run(self):
        self.index_functions(self.root)
        try:
            self.execute(self.root) 
        except ExitSignal:
            raise Exception("Runtime Error: 'exit' used outside of a loop.")
        except NextSignal:
            raise Exception("Runtime Error: 'continue' used outside of a loop.")