



class Statements:
    pass

class VariableStatement:
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
class LetStatement(VariableStatement):
    def __repr__(self):
        return f"Let {self.variable} = {self.value}"
class AssignStatement(VariableStatement):
    def __repr__(self):
        return f"Assign {self.variable} = {self.value}"

class SayStatement(Statements):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Print {self.value}"

class IfStatement(Statements):
    def __init__(self, condition, statements, else_branch=None):
        self.condition = condition
        self.statements = statements
        self.else_branch = else_branch
    def __repr__(self):
        return f"Condition: {self.condition}"
        
class Block():
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"{self.statements}"
class Scope():
    def __init__(self, variables, parent=None):
        self.variables = variables
        self.parent = parent
        
class WhileStatement:
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements
    def __repr__(self):
        return f"While {self.condition} Do {self.statements}"

class ExitStatement:
    pass

class NextStatement:
    pass
 
class ReturnStatement:
    def __init__(self, value=None):
        self.value = value

class Function:
    def __init__(self, name, parameters=None, statements=None):
        self.name = name
        self.statements = statements or []
        self.parameters = parameters or []
    def __repr__(self):
        return f"Name: {self.name}, Parameters: {self.parameters}, statements: {self.statements}"
        
class FunCall:
    def __init__(self, name, arguments=None):
        self.name = name
        self.arguments = arguments or []
    def __repr__(self):
        return f"Name: {self.name}, arguments: {self.arguments}"