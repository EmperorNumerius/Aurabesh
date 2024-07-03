class CommonFunctions:
    def execute(self, command):
        if command.startswith("Option"):
            self.option_choice(command)
        elif command.startswith("UniqueFunction"):
            self.unique_function()
        # Implement other common functions

    def set_variable(self, command):
        parts = command.split("Set")[1].strip().split("=")
        var_name = parts[0].strip()
        var_value = eval(parts[1].strip().rstrip(";"))
        globals()[var_name] = var_value
        print(f"{var_name} set to {var_value}")

    def transmit_command(self, command):
        message = command.split("Transmit")[1].strip().strip(';')
        print(message)

    def option_choice(self, command):
        parts = command.split("Option")[1].strip().split(":")
        condition = parts[0].strip()
        if_true = parts[1].strip()
        if_false = parts[2].strip()
        if eval(condition):
            print(if_true)
        else:
            print(if_false)

    # Add the unique and extremely useful function
    def unique_function(self):
        print("Executing unique function!")
