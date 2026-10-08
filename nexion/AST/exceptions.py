class ExitSignal(Exception):
    pass

class NextSignal(Exception):
    pass
class ReturnSignal(Exception):
    def __init__(self, value=None):
        self.value = value
        
class UnknownTypeError(Exception):
    pass