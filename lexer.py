INTEGER, PLUS, MINUS, MUL, DIV, EOF, LEFT, RIGHT, LOG, SIN, COS, TAN, CTG, SQRT, POW, COMMA, GREATER, LESS\
         , GREATER_E, LESS_E, EQUALS, EQUALS_I, EQUALS_NOT, VAR, D_VAR, FLOAT, TRUE, FALSE = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'EOF', 'LEFT', 'RIGHT',
    'LOG', 'SIN', 'COS', 'TAN', 'CTG', 'SQRT', 'POW', ',', '>', '<',
    '>=', '<=', '=', '==', '!=', 'VAR', 'D_VAR', 'FLOAT', 'True', 'False'
)

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS, MUL, DIV, or EOF
        self.type = type
        # token value: non-negative integer value, '+', '-', '*', '/', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()
		
		
class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "3 * 5", "12 / 3 * 4", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            result += '.'
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            db = float(result)
            return round(db, 3)
        else:
            return int(result)

    def getFunToken(self, fun, length):
        i = 0;
        result = ''
        while (i<length):
            result += self.current_char
            self.advance()
            i+=1
        if fun == 'C':
            if result.upper() == 'COS' or result.upper() == 'CTG':
                return result.upper()
            else:
                self.error()
                return 0
        if fun == 'S':
            if result.upper() == 'SIN':
                return result.upper()
            elif result.upper() == 'SQR':
                result += self.current_char
                self.advance()
                if result.upper() == 'SQRT':
                    return result.upper();
                else:
                    return 0
            else:
                return 0
        if result.upper() == fun:
            return fun
        else:
            self.error()
            return 0

    def getIdentityToken(self, identity):
        if self.pos + 1 < len(self.text):
            self.advance()
            if self.current_char == '=':
                return identity+'='
            else:
                return identity
        else:
            return 0

    def getVar(self):
        startPos = self.pos
        tempPos = 0
        result = ''
        test = 0
        while self.current_char!=None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        tempPos = self.pos
        self.skip_whitespace()
        if self.current_char == '=':
            test += 1
            self.advance()
            self.skip_whitespace()
            if self.current_char == '=':
                test += 1
        if test == 1:
            return result+'='
        elif test == 0:
            if result.upper() in ('SIN', 'COS', 'CTG', 'TAN', 'LOG', 'SQRT', 'POW') and self.current_char == '(':
                self.pos = startPos
                self.current_char = self.text[self.pos]
                return 0
            else:
             return result
        elif test == 2:
            self.pos = tempPos
            self.current_char = self.text[self.pos]
            return result

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                test = self.integer()
                if isinstance(test, int):
                    return Token(INTEGER, test)
                elif isinstance(test, float):
                    return Token(FLOAT, test)

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LEFT, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RIGHT, ')')

            if self.current_char == '>':
                result = self.getIdentityToken('>')
                if result == '>':
                    return Token(GREATER, '>')
                elif result == '>=':
                    self.advance()
                    return Token(GREATER_E, '>=')

            if self.current_char == '<':
                result = self.getIdentityToken('<')
                if result == '<':
                    return Token(LESS, '<')
                elif result == '<=':
                    self.advance()
                    return Token(LESS_E, '>=')

            if self.current_char != None and self.current_char.isalpha():
                result = self.getVar()
                if result != 0 and result[len(result)-1] == '=':
                    result = result[:len(result)-1]
                    return Token(D_VAR, result)
                elif result != 0:
                    if result == 'True':
                        return Token(TRUE, 'True')
                    elif result == 'False':
                        return Token(FALSE, 'False')
                    else:
                        return Token(VAR, result)

            if self.current_char == 'L' or self.current_char == 'l':
                return Token(LOG, self.getFunToken('LOG', 3))

            if self.current_char == 'S' or self.current_char =='s':
                result  = self.getFunToken('S', 3)
                if result == 'SIN':
                    return  Token(SIN, result)
                else:
                    return Token(SQRT, result)

            if self.current_char == 'C' or self.current_char == 'c':
                result = self.getFunToken('C', 3)
                if result == 'COS':
                    return Token(COS, result)
                else:
                    return Token(CTG, result)

            if self.current_char == 'T' or self.current_char == 't':
                return Token(TAN, self.getFunToken('TAN', 3))

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == 'P' or self.current_char == 'p':
                return Token(POW, self.getFunToken('POW', 3))

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(EQUALS_I, '==')
                else:
                    return Token(EQUALS, '=')

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(EQUALS_NOT, '!=')
                else:
                    self.error()

            self.error()

        return Token(EOF, None)