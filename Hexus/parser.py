class NumberNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"NumberNode({self.value})"

class VariableNode:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"VariableNode({self.name})"

class SendCommandNode:
    def __init__(self, text_value, target):
        self.text_value = text_value
        self.target = target

    def __repr__(self):
        return f"SendCommandNode(text={self.text_value}, target={self.target})"
class ReadCommandNode:
    def __init__(self, text_value, var_name, target):
        self.text_value = text_value
        self.var_name = var_name
        self.target = target

    def __repr__(self):
        return f"ReadCommandNode(text={self.text_value}, var={self.var_name}, target={self.target})"

class StopNode:
    def __repr__(self):
        return f"StopNode()"

class ComNode:
    def __init__(self, text_value):
        self.text_value = text_value
    def __repr__(self):
        return f"ComNode(text={self.text_value})"

class SetVar:
    def __init__(self, var_name, value, list):
        self.var_name = var_name
        self.value = value
        self.list = list

    def __repr__(self):
        return f"SetVarNode(var={self.var_name}, value={self.value}, list={self.list})"

class BinaryOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinaryOpNode({self.left} {self.op} {self.right})"

class StringNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"StringNode({self.value})"

class IfNode:
    def __init__(self, exp, value, value2=None, elifv=None):
        self.value = value
        self.exp = exp
        self.value2 = value2
        self.elifv = elifv
    def __repr__(self):
        return f"IfNode(exp={self.exp} value={self.value} value2={self.value2} elifv={self.elifv})"

class HexusParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset=0):
        if self.pos + offset <len(self.tokens):
            return self.tokens[self.pos + offset]
        return ("EOF", "EOF")

    def consume(self, expected_type):
        token_type, value = self.peek()

        if token_type == expected_type:
            self.pos += 1
            return value
        else:
            raise SyntaxError(
                f"Expected token of type '{expected_type}', "
                f"but found '{token_type}' with value '{value}' at position {self.pos}."
            )

    def advance(self):
        token_type, value = self.peek()
        self.pos += 1
        return str(value)

    def consume_value(self, expected_type, expected_value):
        token_type, value = self.peek()
        if token_type == expected_type and value == expected_value:
            self.pos += 1
            return value
        else:
            raise SyntaxError(
                f"Syntax error: Expected '{expected_value}', but found '{value}'."
            )

    def consume_end_of_statement(self):
        token_type, _ = self.peek()
        if token_type == "NEWLINE":
            self.consume("NEWLINE")
        elif token_type == "EOF":
            pass
        else:
            raise SyntaxError(f"SynaxError: Expected end of line, but found token of type '{token_type}'")

    def parse_value(self):
        token_type, value = self.peek()

        if token_type == "INT":
            self.consume("INT")
            value = int(value)
            return NumberNode(value)
        elif token_type == "VAR":
            self.consume("VAR")
            return VariableNode(value)
        elif token_type == "STRING":
            self.consume("STRING")
            return StringNode(value)
        else:
            raise SyntaxError(f"SyntaxError: Expect number or variable, but found '{token_type}' ('{value}')")

    def parse_expression(self):

        token_type, value = self.peek()
        if token_type == "STRING":
            val = self.consume("STRING")
            val = val.split()
            return StringNode(val)
        left = self.parse_value()

        while True:
            next_type, value = self.peek()

            if next_type in ["PLUS", "MINUS", "MUL", "DIV"]:
                self.consume(next_type)
                op = {
                    "PLUS": "+",
                    "MINUS": "-",
                    "MUL": "*",
                    "DIV": "/"
                }[next_type]

                right = self.parse_value()
                left = BinaryOpNode(left, op, right)
            elif next_type == "EQUALS" or (next_type == "KEYWORD" and value == "is"):
                self.consume(next_type)
                op = "=="
                right = self.parse_value()
                left = BinaryOpNode(left, op, right)
            else:
                break
        return left

    def parse_var(self):
        list = False
        var_name = self.consume("VAR")

        token_type, value = self.peek()

        expr_value = None
        if token_type == "EQUAL":
            self.consume("EQUAL")


        elif token_type == "KEYWORD" and value == "is":
            self.consume_value("KEYWORD", "is")

        else:
            raise SyntaxError(f"SyntaxError: Expected '=' or 'is', but found {token_type} ('{value}')")

        if self.peek()[0] == "LSBRACE":
            self.consume("LSBRACE")
            if self.peek()[0] == "RSBRACE":
                self.consume("RSBRACE")
                list = True
        elif self.peek(1)[0] == "COMMA":
            list = True
            expr_value = []
            expr_value.append(self.parse_expression())
            while self.peek()[0] != "NEWLINE" and self.peek()[0] != "EOF":
                self.consume("COMMA")
                if self.peek()[0] == "STRING" or self.peek()[0] ==  "INT" or self.peek()[0] ==  "VAR":
                    expr_value.append(self.parse_expression())

        else:
            expr_value = self.parse_expression()

        self.consume_end_of_statement()
        return SetVar(var_name, expr_value, list)



    def parse_send(self):
        target = "console"
        self.consume("KEYWORD")
        text = self.parse_expression()
        token_type, value = self.peek()
        if token_type == "KEYWORD" and value == "to":
            self.consume_value("KEYWORD", "to")
            target = self.consume("VAR")
        self.consume_end_of_statement()
        return SendCommandNode(text, target)

    def parse_read(self):
        target = "console"
        self.consume("KEYWORD")
        text = self.parse_expression()
        self.consume_value("KEYWORD", "to")
        var = self.consume("VAR")
        token_type, value = self.peek()
        if token_type == "KEYWORD" and value == "from":
            self.consume_value("KEYWORD", "from")
            target = self.consume("VAR")
        self.consume_end_of_statement()
        return ReadCommandNode(text, var, target)

    def parse_stop(self):
        self.consume("KEYWORD")
        self.consume_end_of_statement()
        return StopNode()

    def parse_com(self):
        text = []
        self.consume("HASH")
        while self.peek()[0] != "NEWLINE" and self.peek()[0] != "EOF":
            text.append(self.advance())
        self.consume_end_of_statement()
        return ComNode(" ".join(text))

    def parse_if(self):
        self.consume_value("KEYWORD", "if")
        exp = self.parse_expression()
        value = self.parse_block()
        self.consume_end_of_statement()
        elifv = {}
        while self.peek()[0] == "KEYWORD" and self.peek()[1] == "elif":
            self.consume_value("KEYWORD", "elif")
            elexp = self.parse_expression()
            elvalue = self.parse_block()
            elifv[elexp] = elvalue
            self.consume_end_of_statement()
        value2 = None
        if self.peek()[0] == "KEYWORD" and self.peek()[1] == "else":
            self.consume_value("KEYWORD", "else")
            value2 = self.parse_block()
        self.consume_end_of_statement()
        return IfNode(exp, value, value2, elifv)

    def parse_block(self):
        self.consume("LBRACE")

        while self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")

        statements = []

        while self.peek()[0] != "RBRACE":
            node = self.parse_statement()
            statements.append(node)

            while self.peek()[0] == "NEWLINE":
                self.consume("NEWLINE")

        self.consume("RBRACE")
        return statements

    def parse_statement(self):
        while self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")

        token_type, value = self.peek()

        if token_type == "KEYWORD" and value == "send":
            return self.parse_send()
        elif token_type == "KEYWORD" and value == "read":
            return self.parse_read()
        elif token_type == "KEYWORD" and value == "stop":
            return self.parse_stop()
        elif token_type == "INT" or token_type == "VAR":
            next_type, next_value = self.peek(1)
            if token_type == "VAR" and (next_type == "EQUAL" or (next_type == "KEYWORD" and next_value == "is")):
                return self.parse_var()
            else:
                return self.parse_expression()
        elif token_type == "HASH" and value == "#":
            return self.parse_com()
        elif token_type == "KEYWORD" and value == "if":
            return self.parse_if()
        else:
            raise SyntaxError(f"Unknown start instruction: {token_type} ('{value}')")

    def parse(self):
        program_nodes = []
        while self.peek()[0] != "EOF":
            if self.peek()[0] == "NEWLINE":
                self.consume("NEWLINE")
                continue

            node = self.parse_statement()
            program_nodes.append(node)


        return program_nodes
