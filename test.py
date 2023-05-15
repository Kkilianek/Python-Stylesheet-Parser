from lexer import Lexer
from parser import Parser

text_file_good = open("./good.txt", "r")
good_string = text_file_good.read()
text_file_good.close()

text_file_bad = open("./bad.txt", "r")
bad_string = text_file_bad.read()
text_file_bad.close()


if __name__ == '__main__':
    lexer = Lexer(good_string)
    print(lexer.tokens)

    parser = Parser(lexer)
    parser.start()

