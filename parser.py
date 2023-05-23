# Autor: Kacper Kilianek
# plik z parserem umożliwiającym parsowanie
from lexer import Lexer


class Parser:
    def __init__(self, lexer: Lexer):
        self.next_token = lexer.next_token
        self.token = self.next_token()

    def take_token(self, token_type: str):
        if self.token.type != token_type:
            self.error("Unexpected token: %s" % token_type)
        if token_type != 'EOF':
            self.token = self.next_token()

    def error(self, msg: str):
        line_num = self.token.line
        raise RuntimeError('Parser error, %s on line %d' % (msg, line_num))

    def start(self):
        if self.token.type in ['CLASS', 'ID', 'STRING', 'ASTERISK', 'COMMENT']:
            self.stylesheet()
            self.take_token('EOF')
        else:
            self.error("Start of stylesheet expected but got %s" % self.token.type)

    def stylesheet(self):
        if self.token.type != 'EOF':
            self.statements()
            self.stylesheet()

    def statements(self):
        if self.token.type == 'COMMENT':
            self.take_token(self.token.type)
        else:
            self.selector_block()

    def selector_block(self):
        comma = False
        first_iteration = True
        line_num = self.token.line
        while self.token.type in ['STRING', 'ASTERISK', 'SPECIAL', 'ASSIGN', 'CLASS', 'ID', 'OPERATOR', 'DEDENT',
                                  'COMMENT']:
            if self.token.type in ['STRING', 'CLASS', 'ID']:
                if not comma and not first_iteration and self.token.line != line_num:
                    self.error("Missing comma")
                first_iteration = False
                line_num = self.token.line
            self.take_token(self.token.type)
            if self.token.type == 'OPERATOR':
                self.take_token(self.token.type)
                if self.token.type in ['STRING', 'ASTERISK']:
                    self.take_token(self.token.type)
                else:
                    self.error("Invalid value after operator")
            if self.token.type == 'COMMA':
                comma = True
                self.take_token('COMMA')
        self.declaration_block()

    def declaration_block(self, recurrence: bool = True):
        if self.token.type == 'COMMENT':
            self.take_token('COMMENT')
        if self.token.type == 'DEDENT':
            return
        recurrence = self.declaration(recurrence)
        if self.token.type == 'ASSIGN':
            self.take_token('ASSIGN')
            self.value()
        else:
            self.error("Missing ASSIGN OPERATOR (':')")
        if self.token.type != 'DEDENT' and self.token.type != 'EOF':
            self.declaration_block(recurrence)

    def declaration(self, first_time: bool) -> bool:
        if not first_time:
            if self.token.type == 'STRING':
                self.take_token('STRING')
            else:
                self.error("Invalid declaration beginning")
            return False
        if self.token.type == 'INDENT' and first_time:
            self.take_token('INDENT')
            if self.token.type == 'STRING':
                self.take_token('STRING')
            else:
                self.error("Invalid declaration beginning")
            return False
        else:
            self.error("Missing indent")

    def value(self):
        while self.token.type in ['STRING', 'IMPORTANT', 'NUMBER', 'SPECIAL', 'COLOR', 'PARENTHESIZED']:
            self.take_token(self.token.type)

        if self.token.type == 'END':
            self.take_token('END')
            # print("value OK")
        elif self.token.type != 'DEDENT':
            self.error("Missing END token (;)")
