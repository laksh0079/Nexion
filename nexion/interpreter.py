from AST.program import Program
from AST.statements import LetStatement, AssignStatement, SayStatement, IfStatement, Block, Scope, WhileStatement, NextStatement, ExitStatement, Function, FunCall, ReturnStatement
from AST.exceptions import NextSignal, ExitSignal, ReturnSignal
from AST.expressions import StringLiteral, NumberLiteral, FloatLiteral, Identifier, BinaryExpression, BooleanLiteral, UnaryExpression, NoneLiteral, ListLiteral, IndexExpression, IndexAssignment, DictLiteral, SliceExpression
from operators import OPERATOR_BEHAVIOUR, UNARY_BEHAVIOUR
from stdlib import length, get_type, to_string
class Interpreter:
    def __init__(self, root):
        self.root = root
        self.global_scope = Scope({})
        self.current_scope = self.global_scope
        self.functions = {
            "length": length,
            "typeOf": get_type,
            "toString": to_string
       }
        self.MATH_OPERATORS = {"+", "-", "*", "/", "%"}
        
    def apply_operator(self, left, mid, right):
        if mid in ["+","-","*","/"]:
            if get_type(left) == "boolean" or get_type(right) == "boolean":
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
    
    def validate_index(self, target, index):
        if not get_type(target) in ["list", "dict", "string"]:
                raise Exception(f"Runtime Error: '{get_type(target)}' is not indexable")
        if get_type(target) == "list":
            if not get_type(index) == "int":
                raise Exception("Runtime Error: Index Can Only Be Of Type Int")
            if not 0 <= index < len(target):
                raise Exception("Runtime Error: Index Out of Range")
        elif get_type(target) == "dict":
            if not get_type(index) in ["boolean", "int", "string"]:
                raise Exception("Runtime Error: Dictionary key can only be of type string, int and boolean")
        elif get_type(target) == "string":
            if not get_type(index) == "int":
                raise Exception("Runtime Error: Index Can Only Be Of Type Int")
            if not 0 <= index < len(target):
                raise Exception("Runtime Error: Index Out of Range")
    
    
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
            elif arg is True:
                print("true")
            elif arg is False:
                print("false")
            else:
                print(arg)
        elif type(node) is IfStatement:
            res = self.evaluate(node.condition)
            if get_type(res) != "boolean":
                raise Exception(f"Runtime Error: If condition must be boolean, got {get_type(res)}")
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
                if not get_type(condition) == "boolean":
                    raise Exception(f"Runtime Error: While condition must be boolean, got {get_type(condition)}")
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
        elif type(node) is FloatLiteral:
            return node.value
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
            if node.root == "in":
                if get_type(right) not in ["list", "dict", "string"]:
                    raise Exception("Runtime Error: Right operand of 'in' must be a list, dictionary or string")
                
            if node.root in self.MATH_OPERATORS:
                if get_type(left) == "none" or get_type(right) == "none":
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
            func = self.functions[node.name.name]
            func_name = node.name.name
            if func_name not in self.functions:
                raise Exception(f"Runtime Error: The Function {func_name} Does Not Exist")
            func = self.functions[func_name]
            if callable(func):
                arguments = [self.evaluate(argument) for argument in node.arguments]
                return func(*arguments)
            else:
                #if not func in self.functions:
                   # raise Exception(f"Runtime Error: The Function {node.name} Does Not Exist")
                    #arguments = node.arguments
                var_list = {}
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
            target = self.evaluate(node.target)
            index = self.evaluate(node.index)
            
            self.validate_index(target, index)
            if get_type(target) in ["list", "string"]:
                return target[index]
            elif get_type(target) == "dict":
                if index not in target:
                    raise Exception("Runtime Error: Dictionary Key Not Found")
                return target[index]
                
        elif type(node) is IndexAssignment:
            target = self.evaluate(node.target.target)
            index = self.evaluate(node.target.index)
            self.validate_index(target, index)
            target[index] = self.evaluate(node.value)
        elif type(node) is SliceExpression:
            target = self.evaluate(node.target)
            start = self.evaluate(node.start)
            end = self.evaluate(node.end)
            if get_type(target) not in ["list", "string"]:
                raise Exception("Runtime Error: Index Slicing Can Only Be Done On Type: List or String")
            try:
                if start is None and end is None:
                    return target[:]
                elif start is None:
                    return target[:end]
                elif end is None:
                    return target[start:]
                else:
                    return target[start:end]
            except TypeError:
                raise Exception("Runtime Error: Slice bounds must be integers")
 
    def run(self):
        self.index_functions(self.root)
        try:
            self.execute(self.root) 
        except ExitSignal:
            raise Exception("Runtime Error: 'exit' used outside of a loop.")
        except NextSignal:
            raise Exception("Runtime Error: 'continue' used outside of a loop.")