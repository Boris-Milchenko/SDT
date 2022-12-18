class Operation_Node:
    def __init__(self, operator, options = [None, None], parameters = None):
        self.operator = operator
        self.options = options
        self.parameters = parameters

class Variable_Node:
    def __init__(self, name, value = None):
        self.name = name
        self.value = value

class Value_Node:
    def __init__(self, value):
        self.value = value

class Label_Node:
    def __init__(self, name):
        self.name = name
