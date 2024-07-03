from functions.sith import SithFunctions

class SithSyntax:
    def __init__(self):
        self.functions = SithFunctions()

    def execute_command(self, command, common_functions):
        if command.startswith("Set"):
            common_functions.set_variable(command)
        elif command.startswith("ForceChoke"):
            self.functions.force_choke(command)
        elif command.startswith("Transmit"):
            common_functions.transmit_command(command)
        elif command.startswith("Switch"):
            self.functions.switch_case(command)
        elif command.startswith("ForEach"):
            self.functions.for_each(command)
        elif command.startswith("Try"):
            self.functions.try_catch(command)
        elif command.startswith("While"):
            self.functions.while_loop(command)
        else:
            common_functions.execute(command)
