from Translator.nodes import *

class Parser:
    def __init__(self, tokens = None):
        self.Tokens = tokens
        self.Pos = 0
        self.Expressions = []

    def __match(self, expected):
        if self.Pos < len(self.Tokens):
            current_token = self.Tokens[self.Pos]
            if current_token.kind.name in expected:
                self.Pos += 1
                return current_token
        
        return None

    def __require(self, expected):
        token = self.__match(expected)
        if token == None:
            raise Exception("There is one of: [ %s ] expected on %u position" % (expected, self.Pos))

        return token
    
    def Parse(self, tokens = None):
        self.Expressions.clear()
        self.Pos = 0

        if tokens:
            self.Tokens = tokens

        while self.Pos < len(self.Tokens):
            expression = self.__parse_expression()
            self.__require(('SEP'))
            self.Expressions.append(expression)
        
        return self.Expressions

    def __parse_nest(self):
        start = self.__match(('LNEST',))
        if start:
            nest = self.__parse_formula()
            self.__require(('RNEST',))
            return nest
        return None

    def __parse_valueOrVariable(self, prev = None, compl = 1):
        initiate = self.__match(('VAR', 'VAL', 'DIG', 'LABEL', 'NUM', 'NAME', 'AGE', 'SEX', 'DOMICILE', 'DIAGNOSIS', 'I_M', 'E_M', 'C_M', 'SORT_BY_ASC', 'SORT_BY_DESC'))
        if not initiate:
            return None

        nex = [None, self.__match(('PLETH', 'JOIN'))][compl]
        current = None
        if initiate.kind.name == 'VAR':
            current = Variable_Node(initiate.text)

        elif initiate.kind.name == 'DIG':
            current = Value_Node(int(initiate.text))

        elif initiate.kind.name == 'LABEL':
            current = Label_Node(initiate.text)

        else:
            current = Value_Node(initiate.text)

        nest = self.__parse_nest()
        if nest:
            current = Operation_Node('NEST', parameters = [current, nest])

        if prev != None:
            current = Operation_Node(operator = 'PLETH', parameters = [prev, current])
        if nex:
            if nex.kind.name == 'JOIN':
                return Operation_Node(operator = nex.kind.name, parameters = [current, self.__parse_valueOrVariable()])
            return self.__parse_valueOrVariable(current)
        return current

    def __parse_parentheses(self):
        if self.__match(('LPAR',)):
            node = self.__parse_formula()
            self.__require(('RPAR',))
            return node

        return self.__parse_valueOrVariable()

    def __parse_formula(self):
        operator = self.__match(('NOT',))
        left_node = None
        if operator == None:
            left_node = self.__parse_parentheses()
            operator = self.__match(('PLUS', 'MINUS', 'MUL', 'DIV', 'AND', 'OR',
                                    'G', 'GE', 'E', 'NE', 'L', 'LE'))

        while operator:
            right_node = self.__parse_parentheses()
            left_node = Operation_Node(operator = operator.kind.name, parameters = [left_node, right_node])

            operator = self.__match(('PLUS', 'MINUS', 'MUL', 'DIV', 'AND', 'OR', 
                                    'G', 'GE', 'E', 'NE', 'L', 'LE'))
        return left_node

    # 0 - all, 1 - to CHANGE command
    def __parse_modifier(self, mode = 0):
        if mode == 0:
            start = self.__match(('ALL',))
            if start:
                return Value_Node(start.text)
        else:
            initiate = self.__match(('I_M', 'E_M', 'C_M'))
            s = self.__match(('I_M', 'E_M', 'C_M'))
            while s:
                initiate.text += s.text
                s = self.__match(('I_M', 'E_M', 'C_M'))
            if initiate != None:
                return Value_Node(initiate.text)
            return None

    def __label_as(self):
        label = self.__match(('LABEL',))
        op = None
        if label:
            self.__require(('LABEL_ID',))
            op = Operation_Node('ASSIGN', options=[None, None], parameters=[Label_Node(label.text), None])
        return op

    def __parse_expression(self):
        options = []
        parameters = []
        header = self.__parse_valueOrVariable()
        operator = self.__match(('ASSIGN',))
        if header:
            if operator:
                return Operation_Node('ASSIGN', options=[None, None], parameters = [header, self.__parse_formula()])
            if (self.__match(('LABEL_ID',))):
                return Operation_Node('ASSIGN', parameters = [header, None])

        options.append(header)

        initiate_token = self.__require(('LENGTH', 'CONNECT', 'OPEN', 'GET_TABLES', 'CHANGE', 'ADD', 'SAVE', 'PICK_TO', 'SORT', 
                                         'FILTER', 'DEL', 'VAR', 'HELP', 'QUIT', 'INSERT', 'LOG', 'CALL', 'JMP'))
        initiate_token_name = initiate_token.kind.name
        options.append(self.__parse_modifier())

        if initiate_token_name == 'VAR':
            initiate_token_name = self.__require(('ASSIGN',)).kind.name
            parameters.append(Variable_Node(initiate_token.text))
            parameters.append(self.__parse_formula())

        elif initiate_token_name in ['CALL', 'JMP']:
            parameters.append(self.__parse_valueOrVariable())
            options.append(Value_Node(initiate_token.text[-2:]))

        elif initiate_token_name in ['OPEN', 'QUIT']:
            operand = self.__parse_valueOrVariable()
            while (operand):
                parameters.append(operand)
                operand = self.__parse_valueOrVariable()

            options.append(Value_Node(initiate_token.text))

        elif initiate_token_name == 'SAVE':
            parameters.append(self.__parse_valueOrVariable())

        elif initiate_token_name == 'CHANGE':
            l = 2
            dig = self.__parse_valueOrVariable()
            if dig == None or not isinstance(dig.value, str):
                parameters.append(dig)
                nex = self.__parse_parentheses()
                if not isinstance(nex, Operation_Node):
                    l -= 1
                    parameters.append(None)
                parameters.append(nex)
            else:
                parameters.append(None)
                parameters.append(None)
                parameters.append(dig)
                l = 1
            for i in range(l):
                parameters.append(self.__parse_valueOrVariable(compl = 0))
            num = self.__parse_valueOrVariable(compl=0)
            
            if num != None and not isinstance(num.value, int):
                parameters.append(None)
                parameters.append(num)
            else:
                parameters.append(num)
                parameters.append(self.__parse_modifier(mode = 1))

        elif initiate_token_name == 'PICK_TO':
            num = 1
            destination = self.__parse_valueOrVariable()

            if destination == None or isinstance(destination, Operation_Node) or isinstance(destination.value, int):
                parameters.append(None)
                num -= 1
            parameters.append(destination)

            for i in range(num):
                parameters.append(self.__parse_valueOrVariable())
            parameters.append(self.__parse_formula())
            

        elif initiate_token_name == 'SORT':
            for i in range(2):
                parameters.append(self.__parse_valueOrVariable())
            
        elif initiate_token_name in ['DEL', 'FILTER']:
            parameters.append(self.__parse_valueOrVariable())
            parameters.append(self.__parse_formula())

        elif initiate_token_name == 'INSERT':
            parameters.append(None)
            for i in range(5):
                parameters.append(self.__parse_valueOrVariable())

            parameters = [parameters]

        elif initiate_token_name == 'CONNECT':
            for i in range(4):
                parameters.append(self.__parse_valueOrVariable())

        elif initiate_token_name == 'GET_TABLES':
            parameters.append(self.__parse_valueOrVariable())

        elif initiate_token_name == 'LOG':
            parameters.append(self.__parse_formula())

        return Operation_Node(operator = initiate_token_name, options = options, parameters = parameters)
