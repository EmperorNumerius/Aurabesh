import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens = []

    def tokenize(self):
        rules = [
            ('SET_PATH', r'Set Path ~~> [a-zA-Z]+:/'),
            ('SET_VAR', r'Set [a-zA-Z][a-zA-Z0-9_]* = [^;]+;'),
            ('TRANSMIT', r'Transmit "[^"]+";'),
            ('FORCECHOKE', r'ForceChoke [a-zA-Z0-9\{\}]+;'),
            ('MINDTRICK', r'MindTrick [a-zA-Z0-9\{\}]+;'),
            ('SWITCH', r'Switch [a-zA-Z0-9]+: [a-zA-Z0-9=> ]+;'),
            ('FOREACH', r'ForEach \{.+\}: \{.+\};'),
            ('TRY', r'Try \{.+\}: \{.+\};'),
            ('WHILE', r'While [a-zA-Z0-9<>= ]+: \{.+\};'),
            ('OPTION', r'Option [a-zA-Z0-9<>= ]+: "[^"]+" : "[^"]+";'),
            ('UNIQUE', r'UniqueFunction;'),
            ('BLOCK_START', r'\{'),
            ('BLOCK_END', r'\}'),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+')
        ]

        while self.pos < len(self.text):
            match = None
            for token_type, pattern in rules:
                regex = re.compile(pattern)
                match = regex.match(self.text, self.pos)
                if match:
                    value = match.group(0)
                    if token_type != 'SKIP':
                        self.tokens.append(Token(token_type, value))
                    self.pos = match.end(0)
                    break
            if not match:
                raise SyntaxError(f"Unexpected character: {self.text[self.pos]}")
        return self.tokens
