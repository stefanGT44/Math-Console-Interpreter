from lexer import *
import math

variables = {}

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """
            factor :(POW | SQRT | TAN | CTG | COS | SIN | LOG | ())
        """
        token = self.current_token
        if token.type == TRUE:
            self.eat(TRUE)
            result = True
            return result
        elif token.type == FALSE:
            self.eat(FALSE)
            result = False
            return result
        elif token.type == MINUS:
            self.eat(MINUS)
            result = -self.factor()
            return result
        elif token.type == D_VAR:
            tkn = token
            self.eat(D_VAR)
            return tkn
        elif token.type == VAR:
            result = variables[token.value]
            self.eat(VAR)
            return result
        elif token.type == POW:
            self.eat(POW)
            self.eat(LEFT)
            result = self.test()
            self.eat(COMMA)
            result = pow(result, self.test())
            self.eat(RIGHT)
            return result
        elif token.type == SQRT:
            self.eat(SQRT)
            self.eat(LEFT)
            result = math.sqrt(self.test())
            self.eat(RIGHT)
            return result
        elif token.type == TAN:
            self.eat(TAN)
            self.eat(LEFT)
            result = math.tan(self.test())
            self.eat(RIGHT)
            return result
        if token.type == CTG:
            self.eat(CTG)
            self.eat(LEFT)
            result = 1/math.tan(self.test())
            self.eat(RIGHT)
            return result
        if token.type == COS:
            self.eat(COS)
            self.eat(LEFT)
            result = math.cos(self.test())
            self.eat(RIGHT)
            return result
        elif token.type == SIN:
            self.eat(SIN)
            self.eat(LEFT)
            result = math.sin(self.test())
            self.eat(RIGHT)
            return result
        elif token.type == LOG:
            self.eat(LOG)
            self.eat(LEFT)
            result = math.log10(self.test())
            self.eat(RIGHT)
            return result
        elif token.type == LEFT:
            self.eat(LEFT)
            result = self.test()
            self.eat(RIGHT)
            return result
        elif token.type == FLOAT:
            self.eat(FLOAT)
            return token.value
        else:
            self.eat(INTEGER)
        return token.value

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        result = self.factor()
        if isinstance(result, float):
            result = round(result, 3)

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                num = self.factor()
                if isinstance(result, int) and isinstance(num, int):
                    result = result * num
                else:
                    result = round(result * num, 3)
            elif token.type == DIV:
                self.eat(DIV)
                num = self.factor()
                if isinstance(result, int) and isinstance(num, int):
                    result = int(result / num)
                else:
                    result = round(result / num, 3)

        return result

    def expr(self):
        """Arithmetic expression parser / interpreter.

        >  14 + 2 * 3 - 6 / 2`
        17

        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER
        """
        result = self.term()
        if isinstance(result, Token):
            return result

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result

    def rel(self):
        """rel: expr((> | < | >= | <= | == | !=) expr)*
        """
        counter = 0
        result = self.expr()
        lastResult = result

        while self.current_token.type in (GREATER, LESS, GREATER_E, LESS_E, EQUALS_I, EQUALS_NOT):
            counter += 1
            token = self.current_token
            if token.type == GREATER:
                self.eat(GREATER)
                a = self.expr()
                if counter == 1:
                    result = result > a
                    lastResult = a
                else:
                    if result == True:
                        result = result & (lastResult > a)
            elif token.type == LESS:
                self.eat(LESS)
                a = self.expr()
                if counter == 1:
                    result = result < a
                    lastResult = a
                else:
                    if result == True:
                        result = result & (lastResult < a)
            elif token.type == GREATER_E:
                self.eat(GREATER_E)
                a = self.expr()
                if counter == 1:
                    result = result >= a
                    lastResult = a
                else:
                    if result == True:
                        result = result & (lastResult >= a)
            elif token.type == LESS_E:
                self.eat(LESS_E)
                a = self.expr()
                if counter == 1:
                    result = result <= a
                    lastResult = a
                else:
                    if result == True:
                        result = result & (lastResult <= a)
            elif token.type == EQUALS_I:
                self.eat(EQUALS_I)
                a = self.expr()
                if counter == 1:
                    result = result == a
                    lastResult = a
                else:
                    if result == True:
                        result = result & (lastResult == a)
            elif token.type == EQUALS_NOT:
                self.eat(EQUALS_NOT)
                a = self.expr()
                if counter == 1:
                    result = result != a
                    lastResult = a
                else:
                    if result == True:
                        result = result & (lastResult != a)

        return result

    def test(self):
        result = self.rel()
        if isinstance(result, Token):
            variables[result.value] = self.test()
            return variables[result.value]
        else:
            if self.current_token.type not in (RIGHT, EOF, COMMA):
                self.error()
            return result