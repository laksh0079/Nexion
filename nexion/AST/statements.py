class Statements:
    pass

class SetStatement(Statements):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value


class SayStatement(Statements):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Print {self.value}"