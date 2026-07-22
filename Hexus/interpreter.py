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
        if isinstance(node.value, str):
            words_list = node.value.split()
        else:
            words_list = node.value


        if len(words_list) == 1:
            text = words_list[0][1:-1]
            if text.startswith("{") and text.endswith("}"):
                var_name = text[1:-1]
                if var_name in self.env:
                    return str(self.env.get(var_name))
            return text
        first = words_list[0][1:]
        middle = words_list[1:-1]
        last = words_list[-1][:-1]
        newtxt = [first] + middle + [last]
        for i, t in enumerate(newtxt):
            if t.startswith("{") and t.endswith("}"):
                t = t[1:-1]
                if t in self.env:
                    txt = self.env.get(t)
                    newtxt[i] = str(txt)

        full_txt = " ".join(newtxt)
        return full_txt

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
        if node.target == "console":
            print(result)

    def visit_SetVar(self, node):
        var = node.var_name.strip()
        if node.list == True:
            if node.value == None:
                self.env[var] = []
                return
            elif node.value:
                list = []
                for v in node.value:
                    result = self.visit(v)
                    list.append(result)
                self.env[var] = list
                return
        value = self.visit(node.value)
        self.env[var] = value

    def visit_ReadCommandNode(self, node):
        value = self.visit(node.text_value)
        var = node.var_name.strip()
        if node.target == "console":
            v = input(value)

            if v.isdigit():
                v = int(v)
            else:
                try:
                    v = float(v)
                except ValueError:
                    pass

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


    def visit_ListAddNode(self, node):
        var_name = node.var.name
        current_value = self.env.get(var_name)
        value = self.visit(node.value)
        if isinstance(current_value, list):
            if not node.pos:
                pos = 1
            else:
                pos = self.visit(node.pos)
            pos -= 1
            current_value.insert(pos, value)
            self.env[var_name] = current_value
        else:
            raise NameError(f"Interpreter Error: Variable '{var_name}' (value: {current_value}) is not a list")

    def visit_ListRemoveNode(self, node):
        value = None
        var_name = node.var.name
        current_value = self.env.get(var_name)
        if node.value:
            value = self.visit(node.value)
        if isinstance(current_value, list):
            if node.pos:
                pos = self.visit(node.pos)
                pos -= 1
                current_value.pop(pos)
                self.env[var_name] = current_value
            elif value:
                current_value.remove(value)
                self.env[var_name] = current_value
        else:
            raise NameError(f"Interpreter Error: Variable '{var_name}' (value: {current_value}) is not a list")


    def visit_WaitNode(self, node):
        import time

        value = self.visit(node.value)

        if hasattr(node.value2, "name"):
            value2 = node.value2.name
        else:
            value2 = self.visit(node.value2)

        if value2 == "s":
            time.sleep(value)
        elif value2 == "m":
            time.sleep(value * 60)
        elif value2 == "h":
            time.sleep(value * 60 * 60)
        elif value2 == "d":
            time.sleep(value * 60 * 60 * 24)
        else:
            raise ValueError(f"Unknown wait unit: {value2}")









    def interpret(self, nodes):
        for node in nodes:
            self.visit(node)