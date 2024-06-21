# interpreter.py

class Environment:
    def __init__(self):
        self.variables = {}
        self.functions = {}

class Interpreter:
    def __init__(self):
        self.environment = Environment()
        self.force_path = None

    def interpret(self, program):
        for statement in program.statements:
            self.execute(statement)

    def execute(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.execute(statement)
        elif isinstance(node, VariableDeclaration):
            self.environment.variables[node.identifier] = self.evaluate(node.value)
        elif isinstance(node, FunctionDeclaration):
            self.environment.functions[node.name] = node
        elif isinstance(node, PrintStatement):
            print(self.evaluate(node.value))
        elif isinstance(node, ForLoop):
            self.execute_for_loop(node)
        elif isinstance(node, WhileLoop):
            self.execute_while_loop(node)
        elif isinstance(node, IfStatement):
            self.execute_if_statement(node)
        elif isinstance(node, TryCatchStatement):
            self.execute_try_catch_statement(node)
        elif isinstance(node, SwitchStatement):
            self.execute_switch_statement(node)
        elif isinstance(node, Literal):
            return node.value
        elif isinstance(node, Identifier):
            return self.environment.variables.get(node.name, None)
        elif isinstance(node, BinaryOperation):
            return self.evaluate_binary_operation(node)
        else:
            raise Exception(f"Unknown AST node: {node}")

    def evaluate(self, node):
        if isinstance(node, Literal):
            return node.value
        elif isinstance(node, Identifier):
            return self.environment.variables.get(node.name, None)
        elif isinstance(node, BinaryOperation):
            return self.evaluate_binary_operation(node)
        else:
            raise Exception(f"Unknown AST node: {node}")

    def evaluate_binary_operation(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        if node.operator == '+':
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            return left / right
        elif node.operator == '==':
            return left == right
        elif node.operator == '!=':
            return left != right
        elif node.operator == '<':
            return left < right
        elif node.operator == '>':
            return left > right
        elif node.operator == '<=':
            return left <= right
        elif node.operator == '>=':
            return left >= right
        else:
            raise Exception(f"Unknown operator: {node.operator}")

    def execute_for_loop(self, node):
        self.execute(node.init)
        while self.evaluate(node.condition):
            for statement in node.body:
                self.execute(statement)
            self.execute(node.update)

    def execute_while_loop(self, node):
        while self.evaluate(node.condition):
            for statement in node.body:
                self.execute(statement)

    def execute_if_statement(self, node):
        if self.evaluate(node.condition):
            for statement in node.true_body:
                self.execute(statement)
        elif node.false_body is not None:
            for statement in node.false_body:
                self.execute(statement)

    def execute_try_catch_statement(self, node):
        if self.force_path != 'Sith':
            raise Exception("Try-catch is only allowed for Sith")
        try:
            for statement in node.try_block:
                self.execute(statement)
        except Exception as e:
            for statement in node.catch_block:
                self.execute(statement)

    def execute_switch_statement(self, node):
        if self.force_path != 'Sith':
            raise Exception("Switch statements are only allowed for Sith")
        expression_value = self.evaluate(node.expression)
        matched = False
        for case in node.cases:
            if self.evaluate(case.value) == expression_value:
                matched = True
                for statement in case.body:
                    self.execute(statement)
        if not matched and node.default is not None:
            for statement in node.default:
                self.execute(statement)

    def set_force_path(self, path):
        if path in ('Sith', 'Jedi'):
            self.force_path = path
        else:
            raise Exception("Invalid Force Path")
