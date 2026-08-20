from Hexus.parser import FunctionDefNode, HexusParser
from Hexus.lexer import tokenizer_tokens
from typing import Any, Callable
import importlib
import pkgutil
from Hexus import modules
import re


class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]

        if self.parent:
            return self.parent.get(name)

        raise NameError(f"Variable '{name}' is not defined!!!")

    def set(self, name, value):
        if name in self.vars:
            self.vars[name] = value
            return

        if self.parent and name in self.parent:
            self.parent.set(name, value)
            return

        self.vars[name] = value

    def __contains__(self, name):
        try:
            self.get(name)
            return True
        except NameError:
            return False



class HexusInterpreter:
    def __init__(self):
        self.env = Environment()
        self._register_type1_modules()
        self.timer = 0
        self.timer2 = 0
        self.timerset = False

    def _register_type1_modules(self):
        for _, mod_name, _ in pkgutil.iter_modules(modules.__path__):
            if mod_name.endswith("_ext"):
                continue

            py_mod = importlib.import_module(f".modules.{mod_name}", package=__package__)
            for attr_name in dir(py_mod):
                attr = getattr(py_mod, attr_name)
                if attr_name.endswith("Interpreter") and hasattr(attr, "register_handlers"):
                    attr.register_handlers(self)

    def visit(self, node) -> Any:
        method_name = f"visit_{type(node).__name__}"
        visitor: Callable[[Any], Any] = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node, *args, **kwargs):
        _ = args, kwargs, self
        raise Exception(f"Interpreter error: No visit method defined for {type(node).__name__}")

    def visit_NumberNode(self, node):
        _ = self
        value = str(node.value)
        if "." in value:
            return float(value)
        return int(value)

    def visit_StringNode(self, node):
        value = node.value

        if not isinstance(value, str):
            return value

        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            value = value[1:-1]

        def replace_variable(match):
            expression = match.group(1).strip()

            try:
                tokens = [token for token in tokenizer_tokens(expression) if token[0] != "SKIP"]
                expression_parser = HexusParser(tokens)
                expression_node = expression_parser.parse_expression()
                if expression_parser.peek()[0] != "EOF":
                    raise SyntaxError(f"Unexpected token in interpolation: {expression_parser.peek()[1]}")
                return str(self.visit(expression_node))
            except NameError:
                return match.group(0)

        return re.sub(r"\{([^{}]+)\}", replace_variable, value)

    def visit_VariableNode(self, node):
        if node.name in self.env:
            return self.env.get(node.name)
        raise NameError(f"Variable '{node.name}' is not defined!!!")

    def visit_NowNode(self, node):
        _ = node, self
        import time
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        return now

    def visit_BoolNode(self, node):
        _ = self
        return bool(node.value)


    def visit_BinaryOpNode(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)

        if node.op == "+": return left_val + right_val
        if node.op == "-": return left_val - right_val
        if node.op == "*": return left_val * right_val
        if node.op == "/": return left_val / right_val
        if node.op == "==": return left_val == right_val
        if node.op == "!=": return left_val != right_val
        if node.op == "and": return bool(left_val) and bool(right_val)
        if node.op == "or": return bool(left_val) or bool(right_val)
        if node.op == ">": return left_val > right_val
        if node.op == "<": return left_val < right_val
        if node.op == "<=": return left_val <= right_val
        if node.op == ">=": return left_val >= right_val
        if node.op == "%": return left_val % right_val
        raise ValueError(f"Unknown binary operator: {node.op}")

    def visit_SendCommandNode(self, node):
        result = self.visit(node.text_value)
        if node.target == "console":
            print(result)

    def visit_SetVar(self, node):
        var = node.var_name.strip()
        if node.list is True:
            if node.value is None:
                self.env.set(var, [])
                return
            elif node.value:
                list_val = []
                for v in node.value:
                    result = self.visit(v)
                    list_val.append(result)
                self.env.set(var, list_val)
                return
        value = self.visit(node.value)
        self.env.set(var, value)

    def visit_ReadCommandNode(self, node):
        value = self.visit(node.text_value)
        var = node.var_name.strip()
        v = None
        if node.target == "console":
            v = input(value)

            if v.isdigit():
                v = int(v)
            else:
                try:
                    v = float(v)
                except ValueError:
                    pass

        self.env.set(var, v)

    def visit_ComNode(self, node):
        pass

    def visit_IfNode(self, node):
        exp = self.visit(node.exp)
        if exp:
            for val in node.value:
                self.visit(val)
            return
        elifv = node.elifv
        if elifv:
            for e_exp, e_value in elifv.items():
                if bool(self.visit(e_exp)):
                    for val in e_value:
                        self.visit(val)
                    return

        if node.value2:
            for val in node.value2:
                self.visit(val)


    def visit_ListAddNode(self, node):
        var_name = node.var.name
        current_value = self.env.get(var_name)
        value = self.visit(node.value)
        if isinstance(current_value, list):
            if not node.pos:
                pos = len(current_value) + 1
            else:
                pos = self.visit(node.pos)
            pos -= 1
            current_value.insert(pos, value)
            self.env.set(var_name, current_value)
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
                self.env.set(var_name, current_value)
            elif value:
                current_value.remove(value)
                self.env.set(var_name, current_value)
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


    def visit_WhileNode(self, node):
        while bool(self.visit(node.exp)):
            try:
                for val in node.value:
                    try:
                        self.visit(val)
                    except ContinueException:
                        break
            except BreakException:
                break


    def visit_RepeatNode(self, node):
        value = self.visit(node.value)
        value2 = node.value2
        time = 1
        while time <= value:
            try:
                for val in value2:
                    try:
                        self.visit(val)
                    except ContinueException:
                        break
                time += 1
            except BreakException:
                break

    def visit_ClearNode(self, node):
        _ = node, self
        import subprocess
        import os
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)


    def visit_StopNode(self, node):
        if node.value is None:
            value = None
        else:
            value = self.visit(node.value)
        import sys
        if value is None:
            sys.exit("Program stop")
        else:
            sys.exit(value)


    def visit_MakeNode(self, node):
        var = node.var.strip()
        value = node.value
        current_str = self.env.get(var)
        if value == "lower":
            self.env.set(var, current_str.lower())
        elif value == "upper":
            self.env.set(var, current_str.upper())


    def visit_MinusNode(self, node):
        return -self.visit(node.value)


    def visit_PlusNode(self, node):
        return +self.visit(node.value)


    def visit_NotNode(self, node):
        value = self.visit(node.value)
        return not value


    def visit_LengthNode(self, node):
        var = self.visit(node.var)
        return len(var)

    def visit_TimeNode(self, node):
        _ = self
        import time
        value = node.value
        if value == "hour":
            return time.strftime("%H")
        elif value == "minute":
            return time.strftime("%M")
        elif value == "second":
            return time.strftime("%S")
        else:
            raise NameError(f"Don't know {value}")


    def visit_BreakNode(self, node):
        raise BreakException


    def visit_ContinueNode(self, node):
        raise ContinueException


    def visit_FunctionDefNode(self, node):
        self.env.set(node.name, node)


    def visit_ReturnNode(self, node):
        value = None
        if node.value is not None:
            value = self.visit(node.value)
        raise ReturnException(value)


    def visit_FunctionCallNode(self, node):
        func_node = self.env.get(node.name)
        if not isinstance(func_node, FunctionDefNode):
            raise TypeError(f"'{node.name}' is not a function")
        if len(node.args) != len(func_node.para):
            raise TypeError(f"Function '{node.name}' expects {len(func_node.para)} arguments, but got {len(node.args)}")
        arg_values = [self.visit(arg) for arg in node.args]
        previous_env = self.env
        local_env = Environment(parent=previous_env)
        for para_name, val in zip (func_node.para, arg_values):
            local_env.set(para_name, val)
        self.env = local_env
        return_value = None
        try:
            for stmt in func_node.body:
                self.visit(stmt)
        except ReturnException as ret:
            return_value = ret.value
        finally:
            self.env = previous_env

        return return_value


    def visit_StartTimerNode(self, node):
        _ = node
        import time
        self.timer = time.time()
        self.timerset = False


    def visit_StopTimerNode(self, node):
        _ = node
        import time
        now = time.time()
        self.timer2 = round(now - self.timer)
        self.timerset = True

    def visit_TimerNode(self, node):
        _ = node
        if not self.timerset:
            import time
            now = time.time()
            self.timer2 = round(now - self.timer)
            return self.timer2
        else:
            return self.timer2



    def visit_IndexNode(self, node):
        target = self.visit(node.target)
        pos = self.visit(node.pos)
        try:
            return target[pos - 1]
        except Exception:
            raise TypeError(f"{target} is not a list")


    def visit_RandomNode(self, node):
        value1 = self.visit(node.value1)
        value2 = self.visit(node.value2)
        import random
        return random.randint(value1, value2)



    def visit_ForNode(self, node):
        if hasattr(node.value, "name"):
            var_name = node.value.name
        else:
            raise TypeError("???")
        list_value = self.visit(node.list_value)
        had_var = var_name in self.env.vars
        old_value = self.env.vars.get(var_name)
        try:
            for item in list(list_value):
                self.env.set(var_name, item)
                try:
                    for stmt in node.value2:
                        try:
                            self.visit(stmt)
                        except ContinueException:
                            break
                except BreakException:
                    break
        finally:
            if had_var:
                self.env.vars[var_name] = old_value
            else:
                self.env.vars.pop(var_name, None)

    def visit_VarPlusNode(self, node):
        value = self.visit(node.value)
        var = node.var.strip()

        old_value = self.env.get(var)
        new_value = old_value + int(value)

        self.env.set(var, new_value)

    def visit_VarMinusNode(self, node):
        value = self.visit(node.value)
        var = node.var.strip()

        old_value = self.env.get(var)
        new_value = old_value - int(value)

        self.env.set(var, new_value)



    def visit_NumberForNode(self, node):
        if hasattr(node.var, "name"):
            var_name = node.var.name
        else:
            raise TypeError("???")
        start_value = self.visit(node.value) + 1
        end_value = self.visit(node.value2) + 1
        had_var = var_name in self.env.vars
        old_value = self.env.vars.get(var_name)
        try:
            for item in range(start_value, end_value):
                self.env.set(var_name, item)

                try:
                    for stmt in node.block:
                        try:
                            self.visit(stmt)
                        except ContinueException:
                            break
                except BreakException:
                    break
        finally:
            if had_var:
                self.env.vars[var_name] = old_value
            else:
                self.env.vars.pop(var_name, None)











    def interpret(self, nodes):
        for node in nodes:
            self.visit(node)
