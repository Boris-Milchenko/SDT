class Token_Type:
    def __init__(self, name, regex):
        self.__name = name
        self.__regex = regex

    @property
    def name(self):
        return self.__name

    @property
    def regex(self):
        return self.__regex

class Token:
    def __init__(self, kind, text, pos):
        self.kind = kind
        self.text = text
        self.pos = pos

token_types = {

        'PROPERTY_NUM': Token_Type('NUM', 'num|нумер'),
        'PROPERTY_NAME': Token_Type('NAME', 'name|фамилия'),
        'PROPERTY_SEX': Token_Type('SEX', 'sex|пол'),
        'PROPERTY_AGE': Token_Type('AGE', 'age|возраст'),
        'PROPERTY_DOMICILE': Token_Type('DOMICILE', 'domicile|город'),
        'PROPERTY_DIAGNOSIS': Token_Type('DIAGNOSIS', 'diagnosis|диагноз'),
        'CONNECT': Token_Type('CONNECT', 'connect|подключить'),
        'GET_TABLES': Token_Type('GET_TABLES', 'tables|таблицы'),
        'LOG': Token_Type('LOG', 'echo|эхо'),
        'RUN_FILE': Token_Type('CALL', 'exe|выполнить'),
        'JMPs': Token_Type('JMP', 'jmp|jz|jnz'),
        'OR': Token_Type('OR', 'OR|ИЛИ'),
        'AND': Token_Type('AND', 'AND|И'),
        'OPEN': Token_Type('OPEN', 'new|открыть'),
        'HELP': Token_Type('HELP', 'help|помощь'),
        'BY_ASCENSION': Token_Type('SORT_BY_ASC', 'asc|возр'),
        'BY_DESCENSION': Token_Type('SORT_BY_DESC', 'desc|убыв'),
        'ASSIGN': Token_Type('ASSIGN', 'as|как'),

        'SEPARATOR': Token_Type('SEP', '\||\n'),
        'LABEL_ID': Token_Type('LABEL_ID', '>>'),
        'JOIN': Token_Type('JOIN', '\,'),
        'PLETHORA': Token_Type('PLETH', '\.\.'),
        'SPACE': Token_Type('SPACE', '\s'),
        'LPAR': Token_Type('LPAR', '\('),
        'RPAR': Token_Type('RPAR', '\)'),
        'LNEST': Token_Type('LNEST', '\['),
        'RNEST': Token_Type('RNEST', '\]'),
        'NOT_EQUAL': Token_Type('NE', '\!='),
        'LE': Token_Type('LE', '\<='),
        'GE': Token_Type('GE', '\>='),
        'GREATER': Token_Type('G', '\>'),
        'LOWER': Token_Type('L', '\<'),
        'EQUAL': Token_Type('E', '='),
        'NOT': Token_Type('NOT', '\!'),

        'IMPLICITY_MODE': Token_Type('I_M', 'i|вх'),
        'EXPLICITY_MODE': Token_Type('E_M', 'e|сл'),
        'CONTINUE_MODE': Token_Type('C_M', 'c|пр'),
        'ALL_MODE': Token_Type('ALL', 'a|все'),

        'LENGTH': Token_Type('LENGTH', 'l|дл'),
        'QUIT': Token_Type('QUIT', 'q|Q|в|В'),
        'CHANGE': Token_Type('CHANGE', 'r|з'),
        'INSERT': Token_Type('INSERT', 'n|д'),
        'WRITE': Token_Type('SAVE', 'w|х'),
        'SELECT': Token_Type('PICK_TO', 'p|п'),
        'SORT': Token_Type('SORT', 's|с'),
        'FILTER': Token_Type('FILTER', 'f|ф'),
        'DELETE': Token_Type('DEL', 'd|у'),
        'PLUS': Token_Type('PLUS', '\+'),
        'MINUS': Token_Type('MINUS', '\-'),
        'MULTI': Token_Type('MUL', '\*'),
        'DIVISION': Token_Type('DIV', '\/'),

        'DIGIT': Token_Type('DIG', '(-)*\d+'),
        'VAR': Token_Type('VAR', '\$[^\s\|\$\[\]]+'),
        'USER_VALUE': Token_Type('VAL', '(~|Ё ).*?(~| Ё)'),
        'LABEL': Token_Type('LABEL', '[^\s>\|]+')
        }
