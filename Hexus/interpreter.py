class HexusInterpreter:
    def __init__(self):
        self.env = {}

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"Interpreter error: No visit method defined for {type(node).__name__}")


    def visit_NumberNode(self, node):
        return int(node.value)

    def visit_StringNode(self, node):
        return node.value[1:-1]

    def visit_VariableNode(self, node):
        if node.name in self.env:
            return self.env[node.name]
        raise NameError(f"Variable '{node.name}' is not defined!!!")


    def visit_BinaryOpNode(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)

        if node.op == "+": return left_val + right_val
        if node.op == "-": return left_val - right_val
        if node.op == "*": return left_val * right_val
        if node.op == "/": return left_val / right_val
        if node.op == "==": return left_val == right_val

    def visit_SendCommandNode(self, node):
        result = self.visit(node.text_value)
        print(result)

    def visit_SetVar(self, node):
        value = self.visit(node.value)
        var = node.var_name.strip()
        self.env[var] = value

    def visit_ReadCommandNode(self, node):
        value = self.visit(node.text_value)
        var = node.var_name.strip()
        v = input(value)

        if v.isdigit():
            v = int(v)

        self.env[var] = v

    def visit_ComNode(self, node):
        pass

    def visit_IfNode(self, node):
        exp = self.visit(node.exp)
        if exp == True:
            value = node.value
            while value:
                val = value.pop(0)
                self.visit(val)
            return
        elifv = node.elifv
        if elifv:
            for exp, value in elifv.items():
                exp = self.visit(exp)
                if exp == True:
                    while value:
                        val = value.pop(0)
                        self.visit(val)
                    return

        if node.value2:
            value2 = node.value2
            while value2:
                val = value2.pop(0)
                self.visit(val)









    def interpret(self, nodes):
        for node in nodes:
            self.visit(node)