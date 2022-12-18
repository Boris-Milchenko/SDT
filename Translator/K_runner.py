from Translator.nodes import *
from sources import Columns, int_cols

class Runner:
    def __init__(self, app, expressions = None):
        self.Pos = 0
        self.App = app
        self.Variables = {'wd': self.App.Csv.wd}
        self.Labels = {}
        self.Expressions = expressions

        self.Flags = {'z': False}
        self.obj = None

        self.Do = {
                'LENGTH': self.__len,
                'HELP': self.__help,
                'ASSIGN': self.__assign,
                'DEL': self.__del,
                'OPEN': self.__open,
                'CONNECT': self.__connect,
                'GET_TABLES': self.__get_tables,
                'LOG': self.__log,
                'INSERT': self.__insert,
                'PLETH': self.__pleth,
                'JOIN': self.__join,
                'SAVE': self.__save,
                'CHANGE': self.__change,
                'PICK_TO': self.__pick,
                'QUIT': self.__quit,
                'SORT': self.__sort,
                'FILTER': self.__filter,
                'ASSIGN': self.__assign,
                'JMP': self.__jumps,
                'CALL': self.__call,
                }

        self.LaMA = {
                'E': lambda x, y: x == y,
                'NE': lambda x, y: x != y,
                'G': lambda x, y: x > y,
                'L': lambda x, y: x < y,
                'GE': lambda x, y: x >= y,
                'LE': lambda x, y: x <= y,
                'AND': lambda x, y: x and y,
                'OR': lambda x, y: x or y,
                'NOT': lambda x, y: not y,
                'PLUS': lambda x, y: x + y,
                'MINUS': lambda x, y: x - y,
                'MUL': lambda x, y: x * y,
                'DIV': lambda x, y: x / y,
                }

    def Run(self, expressions = None):
        self.Pos = 0

        if expressions:
            self.Expressions = expressions
        while self.Pos < len(self.Expressions):
            self.run(self.Expressions[self.Pos])
            self.Pos += 1

    def run(self, expression, subst = None):
        if isinstance(expression, Operation_Node):
            if expression.operator in self.LaMA.keys():
                return self.__lama(expression.operator, parameters = expression.parameters, subst = subst)
            elif expression.operator == 'NEST':
                return self.__valueOrVariable(expression, subst)

            options = []
            if expression.options != None:
                for option in expression.options:
                    options.append(self.run(option))
                if options[1] == None:
                    options[1] = ''
                self.obj = options[0]

            return self.Do[expression.operator](options, expression.parameters)
        else:
            return self.__valueOrVariable(expression, subst = subst)

#---------------------------------------------------------------------------------------
# HELPFUL, BUT NOT EXECUTIVE

    def __nest(self, nest_kit):
        nested = self.run(nest_kit[0])
        descr = self.run(nest_kit[1])
        return nested, descr

    def __add_to_list(self, to, *whats):
        for what in whats:
            if not isinstance(what, (set, list, tuple)):
                if what not in to:
                    to.append(what)
            else:
                for i in what:
                    if not i in to:
                        to.append(i)

    def __join(self, options, parameters):
        scope = []
        left = self.run(parameters[0])
        right = self.run(parameters[1])
        self.__add_to_list(scope, left, right)

        return scope

    def __pleth(self, options, parameters):
        scope = []
        left = self.run(parameters[0])
        right = self.run(parameters[1])
        for i in range(left, right + 1):
            if not i in scope:
                scope.append(i)

        return scope
        
    def __lama(self, operator, parameters, subst = None):
        num = len(parameters)
        pars = [0]*num
        for i in range(num):
            pars[i] = self.run(parameters[i], subst = subst)

        result = self.LaMA[operator](*pars)
        self.Flags['z'] = result == 0
        return result

    def __valueOrVariable(self, node, subst = None):
        if not node:
            return None
        if isinstance(node, Operation_Node) and node.operator == 'NEST':
            nested, descr = self.__nest(node.parameters)
            if isinstance(nested, int):
                current = int(str(nested)[descr])
            else:
                current = nested[descr]

        elif isinstance(node, Variable_Node):
            if node.name.isdigit() or node.name in Columns[self.App.lang].keys():
                current = self.App.Get_Item(self.obj, node.name, node.name.isdigit())
            else:
                current = self.Variables[node.name]

        elif isinstance(node, Label_Node):
            current = self.Labels[node.name]

        else:
            if node.value in Columns[self.App.lang].keys() and subst != None:
                ind = Columns[self.App.lang][node.value]
                current = subst[ind]
                if node.value in int_cols:
                    current = int(current)
            else:
                current = node.value

        return current

    def __read_file(self, file):
        file = self.App.Csv.preprocess_file(file)
        with open(file, 'r') as f:
            return f.read()

#---------------------------------------------------------------------------------------

    def __help(self, options, parameters):
        self.App.manual()

    def __call(self, options, parameters):
        file = self.run(parameters[0])
        self.App.run_command(event = None, command = self.__read_file(file))

    def __quit(self, options, parameters):
        titles = []
        for parameter in parameters:
            titles.append(self.__valueOrVariable(parameter))
        self.App.Quit(options[2], titles, options[1])

    def __assign(self, options, parameters):
        if parameters[1] == None:
            self.Labels[parameters[0].name] = self.Pos
            return

        value = self.run(parameters[1])
        if isinstance(parameters[0], Operation_Node) and parameters[0].operator == 'NEST':
            nested, descriptor = self.__nest(parameters[0].parameters)
            nested[descriptor] = value
            return
        if parameters[0].name == 'wd':
            self.Variables['wd'] = self.App.Csv.Cwd(value)
            return
        self.Variables[parameters[0].name] = value

    def __jumps(self, options, parameters):
        pos = self.run(parameters[0])
        cond = self.Flags[options[2][1]] ^ (options[2][0] in ['n', 'н'])
        if cond:
            self.Pos = pos

    def __open(self, options, parameters):
        titles = []
        for parameter in parameters:
            titles.append(self.__valueOrVariable(parameter))
        self.App.Add_Tables(titles, options[1])

    def __connect(self, options, parameters):
        args = []
        for i in range(len(parameters)):
            args.append(self.run(parameters[i]))
        self.App.Connect(*args)

    def __get_tables(self, options, parameters):
        self.App.Get_Tables(self.run(parameters[0]))

    def __insert(self, options, parameters):
        args = []
        for parameter in parameters:
            args.append([self.run(value) for value in parameter])
        self.App.Insert(options[0], options[1], args)

    def __sort(self, options, parameters):
        column = self.__valueOrVariable(parameters[0])
        order = self.__valueOrVariable(parameters[1])
        self.App.Sort(options[0], options[1], column, order)

    # 0 - move, 1 - copy
    def __save(self, options, parameters):
        destination = self.run(parameters[0])
        self.App.Transfer(source = options[0], dests = destination, modifier = options[1], scope = None, condition = None, mode = '0w')

    def __pick(self, options, parameters):
        args = []
        for i in range(2):
            args.append(self.run(parameters[i]))

        self.App.Transfer(options[0], args[0], options[1], args[1], parameters[2], '1')

    def __change(self, options, parameters):
        args = []
        for i in range(len(parameters)):
            args.append(parameters[i])
            if i != 1:
                args[i] = self.run(parameters[i])

        self.App.Change_Rows(options[0], options[1], *args)

    def __del(self, options, parameters):
        scope = self.run(parameters[0])
        
        self.App.Del(options[0], options[1], scope, parameters[1])

    def __filter(self, options, parameters):
        scope = self.run(parameters[0])
        self.App.Filter(options[0], options[1], scope, parameters[1])

    def __log(self, options, parameters):
        operand = self.run(parameters[0])
        self.App.echo(operand)

    def __len(self, options, parameters):
        self.App.Get_Length(options[0])

