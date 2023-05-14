# Autor: Kacper Kilianek
# plik z lexerem umożliwiającym tokenizację
import collections
import re

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])


class Lexer:
    def __init__(self, text: str):
        self.tokens = []
        self.current_token_number = 0
        self.line_number = 1
        self.indent_levels = [0]
        for token in self.tokenize(text):
            self.tokens.append(token)

    def tokenize(self, text: str):
        tokens = [
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ ]+'),
            ('COLOR', r'\#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})'),
            ('NUMBER', r'[0-9]+'),
            ('IMPORTANT', r'!important'),
            ('COMMENT', r'\/\/.*'),
            ('PARENTHESIZED', r'\((.*?)\)'),
            ('STRING', r'[A-Za-z-]+'),
            ('ID', r'\#[A-Za-z]+'),
            ('CLASS', r'\.[A-Za-z]+'),
            ('OPERATOR', r'[+<>]'),
            ('INDENT', r'\t'),
            ('END', r';'),
            ('ASSIGN', r':'),
            ('COMMA', r','),
            ('ASTERISK', r'\*'),
            ('SPECIAL', r'[#%()"?=_]'),
        ]

        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in tokens)
        get_token = re.compile(tok_regex).match
        current_position = line_start = 0
        last_indent = 0
        match = get_token(text)
        while match is not None:
            type = match.lastgroup
            if type == 'NEWLINE':
                if len(self.tokens) != 0 and self.indent_levels[-1] != 0 and last_indent < self.indent_levels[-1]:
                    self.indent_levels.pop()
                    yield Token('DEDENT', '', self.line_number, match.start() - line_start)
                last_indent = 0  # reset last_indent
                line_start = current_position
                self.line_number += 1
            elif type == 'INDENT':
                last_indent += 1
                counter = 0
                for token in self.tokens:
                    if token.type == 'INDENT' and token.line == self.line_number:
                        counter += 1
                if last_indent > self.indent_levels[-1]:
                    yield Token('INDENT', match.group(type), self.line_number, match.start() - line_start)
                if counter == 0:
                    self.indent_levels.append(last_indent) if last_indent != self.indent_levels[-1] else None
                else:
                    last_indent = counter + 1
                    self.indent_levels.pop()
                    self.indent_levels.append(last_indent)
            elif type == 'COLOR':
                if self.tokens[-1].type == 'ASSIGN' or self.tokens[-1].type == 'STRING':
                    yield Token('COLOR', match.group(type), self.line_number, match.start() - line_start)
                else:
                    yield Token('ID', match.group(type), self.line_number, match.start() - line_start)
            elif type not in ['SKIP', 'INDENT']:
                value = match.group(type)
                yield Token(type, value, self.line_number, match.start() - line_start)
            current_position = match.end()
            match = get_token(text, current_position)
        if current_position != len(text):
            raise RuntimeError('Error: Unexpected character %r on line %d' % \
                               (text[current_position], self.line_number))
        yield Token('EOF', '', self.line_number, current_position - line_start)

    def next_token(self):
        self.current_token_number += 1
        if self.current_token_number - 1 < len(self.tokens):
            return self.tokens[self.current_token_number - 1]
        else:
            raise RuntimeError('Error: No more tokens')
