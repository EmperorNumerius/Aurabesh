from functions.jedi import JediFunctions

class JediSyntax:
    def __init__(self):
        self.functions = JediFunctions()

    def execute_command(self, command, common_functions):
        if command.startswith("Set"):
            common_functions.set_variable(command)
        elif command.startswith("MindTrick"):
            self.functions.mind_trick(command)
        elif command.startswith("Transmit"):
            common_functions.transmit_command(command)
        elif any(command.startswith(blocked) for blocked in ["Switch", "ForEach", "Try", "While"]):
            print("Method is only allowed for Sith programs")
        else:
            common_functions.execute(command)
