from Translator.token import Token, token_types
import re

class Lexer:
    def __init__(self, code = None):
        self.code = code
        self.pos = 0
        self.token_list = []

    def __next_token(self):
        while self.pos < len(self.code):
            string = self.code[self.pos:]
            for token_type in token_types.values():
                regex = token_type.regex
                result = re.match(regex, string)

                if result:
                    result = result.group(0)
                    self.pos += len(result)
                    if token_type.name == 'VAL':
                        result = result[1:-1].strip()
                    elif token_type.name == 'VAR':
                        result = result[1:]
                    if token_type.name != 'SPACE':
                        self.token_list.append(Token(token_type, result, self.pos))
                        #print(token_type.name, result)
                    return True
            return False
    
    def Lex_Analysis(self, code = None):
        self.token_list.clear()
        self.pos = 0

        if code:
            self.code = code
        while self.__next_token():
            pass

        return self.token_list

#l = Lexer()
#l.Lex_Analysis('var as ~k~')
