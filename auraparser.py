# parser.py

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class VariableDeclaration(ASTNode):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

class FunctionDeclaration(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

class PrintStatement(ASTNode):
    def __init__(self, value):
        self.value = value

class ForLoop(ASTNode):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class IfStatement(ASTNode):
    def __init__(self, condition, true_body, false_body=None):
        self.condition = condition
        self.true_body = true_body
        self.false_body = false_body

class TryCatchStatement(ASTNode):
    def __init__(self, try_block, catch_block):
        self.try_block = try_block
        self.catch_block = catch_block

class SwitchStatement(ASTNode):
    def __init__(self, expression, cases, default=None):
        self.expression = expression
        self.cases = cases
        self.default = default

class Case(ASTNode):
    def __init__(self, value, body):
        self.value = value
        self.body = body

class BinaryOperation(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token = None
        self.force_path = None
        self.advance()

    def advance(self):
        if self.next_token is not None:
            self.current_token = self.next_token
        if self.tokens:
            self.next_token = self.tokens.pop(0)
        else:
            self.next_token = Token(TokenType.EOF, '', self.current_token.line if self.current_token else 1, self.current_token.column if self.current_token else 1)

    def parse(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'Set':
                self.set_force_path()
            else:
                statements.append(self.statement())
        return Program(statements)

    def set_force_path(self):
        self.advance()
        self.expect(TokenType.KEYWORD, 'Force')
        self.expect(TokenType.KEYWORD, 'Path')
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value in ('Sith', 'Jedi'):
            self.force_path = self.current_token.value
            self.advance()
        else:
            self.error("Expected 'Sith' or 'Jedi' after 'Set Force Path'")

    def statement(self):
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'print':
            return self.print_statement()
        elif self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'for':
            return self.for_loop()
        elif self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'while':
            return self.while_loop()
        elif self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'if':
            return self.if_statement()
        elif self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'try':
            return self.try_catch_statement()
        elif self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'switch':
            return self.switch_statement()
        elif self.current_token.type == TokenType.IDENTIFIER:
            return self.variable_declaration()
        else:
            self.error(f"Unexpected token: {self.current_token.value}")

    def print_statement(self):
        self.advance()
        value = self.expression()
        self.expect(TokenType.SYMBOL, ';')
        return PrintStatement(value)

    def for_loop(self):
        self.advance()
        self.expect(TokenType.SYMBOL, '(')
        init = self.variable_declaration()
        condition = self.expression()
        self.expect(TokenType.SYMBOL, ';')
        update = self.expression()
        self.expect(TokenType.SYMBOL, ')')
        body = self.block()
        return ForLoop(init, condition, update, body)

    def while_loop(self):
        self.advance()
        self.expect(TokenType.SYMBOL, '(')
        condition = self.expression()
        self.expect(TokenType.SYMBOL, ')')
        body = self.block()
        return WhileLoop(condition, body)

    def if_statement(self):
        self.advance()
        self.expect(TokenType.SYMBOL, '(')
        condition = self.expression()
        self.expect(TokenType.SYMBOL, ')')
        true_body = self.block()
        false_body = None
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'else':
            self.advance()
            false_body = self.block()
        return IfStatement(condition, true_body, false_body)

    def try_catch_statement(self):
        if self.force_path != 'Sith':
            self.error("Try-catch is only allowed for Sith")
        self.advance()
        try_block = self.block()
        self.expect(TokenType.KEYWORD, 'catch')
        catch_block = self.block()
        return TryCatchStatement(try_block, catch_block)

    def switch_statement(self):
        if self.force_path != 'Sith':
            self.error("Switch statements are only allowed for Sith")
        self.advance()
        self.expect(TokenType.SYMBOL, '(')
        expression = self.expression()
        self.expect(TokenType.SYMBOL, ')')
        self.expect(TokenType.SYMBOL, '{')
        cases = []
        default = None
        while self.current_token.type != TokenType.SYMBOL or self.current_token.value != '}':
            if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'case':
                self.advance()
                value = self.expression()
                self.expect(TokenType.SYMBOL, ':')
                body = self.block()
                cases.append(Case(value, body))
            elif self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'default':
                self.advance()
                self.expect(TokenType.SYMBOL, ':')
                default = self.block()
        self.expect(TokenType.SYMBOL, '}')
        return SwitchStatement(expression, cases, default)

    def variable_declaration(self):
        identifier = self.current_token.value
        self.advance()
        self.expect(TokenType.SYMBOL, '=')
        value = self.expression()
        self.expect(TokenType.SYMBOL, ';')
        return VariableDeclaration(identifier, value)

    def expression(self):
        left = self.term()
        while self.current_token.type == TokenType.SYMBOL and self.current_token.value in ('+', '-', '==', '!=', '<', '>', '<=', '>='):
            operator = self.current_token.value
            self.advance()
            right = self.term()
            left = BinaryOperation(left, operator, right)
        return left

    def term(self):
        left = self.factor()
        while self.current_token.type == TokenType.SYMBOL and self.current_token.value in ('*', '/'):
            operator = self.current_token.value
            self.advance()
            right = self.factor()
            left = BinaryOperation(left, operator, right)
        return left

    def factor(self):
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.advance()
            return Literal(float(token.value))
        elif token.type == TokenType.STRING:
            self.advance()
            return Literal(token.value)
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(token.value)
        elif token.type == TokenType.SYMBOL and token.value == '(':
            self.advance()
            expr = self.expression()
            self.expect(TokenType.SYMBOL, ')')
            return expr
        else:
            self.error(f"Unexpected token: {token.value}")

    def block(self):
        self.expect(TokenType.SYMBOL, '{')
        statements = []
        while self.current_token.type != TokenType.SYMBOL or self.current_token.value != '}':
            statements.append(self.statement())
        self.expect(TokenType.SYMBOL, '}')
        return statements

    def expect(self, type, value=None):
        if self.current_token.type != type or (value is not None and self.current_token.value != value):
            self.error(f"Expected {type}({value}), got {self.current_token.type}({self.current_token.value})")
        self.advance()

    def error(self, message):
        raise Exception(f"Parser error at {self.current_token.line}:{self.current_token.column}: {message}")
