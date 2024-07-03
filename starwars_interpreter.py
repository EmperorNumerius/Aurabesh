import sys
from lexer import Lexer
from parser import Parser
from syntax.sith_syntax import SithSyntax
from syntax.jedi_syntax import JediSyntax
from functions.common import CommonFunctions

# Global variables and state
variables = {}
next_command_skipped = False


class StarWarsInterpreter:
    def __init__(self, filepath):
        self.filepath = filepath
        self.path = None
        self.functions = CommonFunctions()

    def set_path(self, path):
        if path.lower() == "sith:/":
            self.path = "Sith"
            self.syntax = SithSyntax()
        elif path.lower() == "jedi:/":
            self.path = "Jedi"
            self.syntax = JediSyntax()
        else:
            raise ValueError("Unknown path")

    def execute(self):
        with open(self.filepath, 'r') as file:
            text = file.read()

        lexer = Lexer(text)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        self.path, commands = parser.parse()
        self.set_path(self.path)

        global next_command_skipped
        for command in commands:
            if next_command_skipped:
                next_command_skipped = False
                continue
            if isinstance(command, tuple) and command[0] == 'BLOCK':
                for subcommand in command[1]:
                    self.syntax.execute_command(subcommand.value, self.functions)
            else:
                self.syntax.execute_command(command.value, self.functions)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python starwars_interpreter.py <filename.sw>")
        sys.exit(1)

    interpreter = StarWarsInterpreter(sys.argv[1])
    interpreter.execute()
