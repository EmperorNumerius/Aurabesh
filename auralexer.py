# lexer.py

import re

class TokenType:
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    KEYWORD = 'KEYWORD'
    SYMBOL = 'SYMBOL'
    WHITESPACE = 'WHITESPACE'
    COMMENT = 'COMMENT'
    EOF = 'EOF'

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'{self.type}({self.value}) at {self.line}:{self.column}'

class Lexer:
    KEYWORDS = {'jedi', 'sith', 'force', 'padawan', 'master', 'if', 'else', 'for', 'while', 'print', 'try', 'catch', 'switch', 'case', 'default'}
    SYMBOLS = {'{', '}', '(', ')', '[', ']', ';', ',', '.', '+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>='}
    WHITESPACE = re.compile(r'\s+')
    IDENTIFIER = re.compile(r'[a-zA-Z_][a-zA-Z_0-9]*')
    NUMBER = re.compile(r'\d+(\.\d+)?')
    STRING = re.compile(r'"([^"\\]|\\.)*"')
    COMMENT = re.compile(r'//.*')

    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_pos = 0
        self.line = 1
        self.column = 1

    def tokenize(self):
        while self.current_pos < len(self.source_code):
            current_char = self.source_code[self.current_pos]

            if self.match(self.WHITESPACE):
                self.consume(self.WHITESPACE)
            elif self.match(self.COMMENT):
                self.consume(self.COMMENT)
            elif current_char in self.SYMBOLS:
                self.add_token(TokenType.SYMBOL, current_char)
                self.advance()
            elif self.match(self.STRING):
                value = self.consume(self.STRING)
                self.add_token(TokenType.STRING, value)
            elif self.match(self.NUMBER):
                value = self.consume(self.NUMBER)
                self.add_token(TokenType.NUMBER, value)
            elif self.match(self.IDENTIFIER):
                value = self.consume(self.IDENTIFIER)
                token_type = TokenType.KEYWORD if value in self.KEYWORDS else TokenType.IDENTIFIER
                self.add_token(token_type, value)
            else:
                self.error(f"Unexpected character: {current_char}")

        self.add_token(TokenType.EOF, '')
        return self.tokens

    def match(self, pattern):
        return bool(re.match(pattern, self.source_code[self.current_pos:]))

    def consume(self, pattern):
        match = re.match(pattern, self.source_code[self.current_pos:])
        if match:
            value = match.group(0)
            self.advance(len(value))
            return value

    def add_token(self, type, value):
        self.tokens.append(Token(type, value, self.line, self.column))

    def advance(self, steps=1):
        for _ in range(steps):
            if self.current_pos < len(self.source_code):
                if self.source_code[self.current_pos] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.current_pos += 1

    def error(self, message):
        raise Exception(f"Lexer error at {self.line}:{self.column}: {message}")
