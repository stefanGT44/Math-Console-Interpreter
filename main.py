from lexer import Lexer
from interpreter import Interpreter
import sys

def main():
    while True:
        try:
            text = input('>>> ')
        except (EOFError, KeyboardInterrupt):
            break
        if text == 'exit':
            sys.exit()
        if not text:
            continue
        try:
            lexer = Lexer(text)
            interpreter = Interpreter(lexer)
            result = interpreter.test()
            print(result)
        except:
            print('Invalid expression!')
            pass


if __name__ == '__main__':
    main()