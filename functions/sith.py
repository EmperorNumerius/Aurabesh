class SithFunctions:
    def force_choke(self, command):
        print("Executing Force Choke!")
        iterable = command.split("ForceChoke")[1].strip().rstrip(';')
        if iterable.startswith("{") and iterable.endswith("}"):
            items = eval(iterable)
            for item in items:
                print(item)
        elif isinstance(iterable, str):
            for char in iterable:
                print(char)

    def switch_case(self, command):
        cases = command.split("Switch")[1].strip().split(":")
        expression = cases[0].strip()
        case_dict = {}
        for case in cases[1:]:
            k, v = case.split("=>")
            case_dict[k.strip()] = v.strip().rstrip(';')
        print(case_dict.get(expression, "Default case"))

    def for_each(self, command):
        parts = command.split("ForEach")[1].strip().split(":")
        iterable = eval(parts[0].strip().rstrip(';'))
        action = parts[1].strip().rstrip('{}').strip()
        for item in iterable:
            exec(action)

    def try_catch(self, command):
        parts = command.split("Try")[1].strip().split(":")
        try_block = parts[0].strip().rstrip('{}').strip()
        except_block = parts[1].strip().rstrip('{}').strip()
        try:
            exec(try_block)
        except Exception as e:
            exec(except_block)

    def while_loop(self, command):
        parts = command.split("While")[1].strip().split(":")
        condition = parts[0].strip()
        action = parts[1].strip().rstrip('{}').strip()
        while eval(condition):
            exec(action)
