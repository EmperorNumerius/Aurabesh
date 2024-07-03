class JediFunctions:
    def mind_trick(self, command):
        print("Executing Mind Trick!")
        iterable = command.split("MindTrick")[1].strip().rstrip(';')
        if iterable.startswith("{") and iterable.endswith("}"):
            items = eval(iterable)
            for item in items:
                print(item)
        elif isinstance(iterable, str):
            for char in iterable:
                print(char)
