class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.path = None

    def parse(self):
        if self.tokens[self.pos].type == 'SET_PATH':
            self.path = self.tokens[self.pos].value.split("~~>")[1].strip()[:-2]
            self.pos += 1
        else:
            raise SyntaxError("Program must start with 'Set Path ~~> [Sith:/|Jedi:/]'")

        commands = []
        while self.pos < len(self.tokens):
            command = self.tokens[self.pos]
            if command.type in ('SET_VAR', 'TRANSMIT', 'FORCECHOKE', 'MINDTRICK', 'SWITCH', 'FOREACH', 'TRY', 'WHILE', 'OPTION', 'UNIQUE'):
                commands.append(command)
                self.pos += 1
            elif command.type == 'BLOCK_START':
                self.pos += 1
                block_commands = []
                while self.tokens[self.pos].type != 'BLOCK_END':
                    block_commands.append(self.tokens[self.pos])
                    self.pos += 1
                commands.append(('BLOCK', block_commands))
                self.pos += 1
            else:
                self.pos += 1
        return self.path, commands
