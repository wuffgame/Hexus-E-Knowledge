import os.path
import os
import importlib.util

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
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"StopNode()"

class ComNode:
    def __init__(self, text_value):
        self.text_value = text_value
    def __repr__(self):
        return f"ComNode(text={self.text_value})"

class SetVar:
    def __init__(self, var_name, value, is_list):
        self.var_name = var_name
        self.value = value
        self.list = is_list

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

class ListAddNode:
    def __init__(self, var, value, pos):
        self.var = var
        self.value = value
        self.pos = pos
    def __repr__(self):
        return f"ListAddNode(var={self.var} value={self.value} pos={self.pos})"

class ListRemoveNode:
    def __init__(self, var, pos, value):
        self.var = var
        self.value = value
        self.pos = pos
    def __repr__(self):
        return f"ListRemoveNode(var={self.var} value={self.value} pos={self.pos}"

class WaitNode:
    def __init__(self, value, value2):
        self.value = value
        self.value2 = value2
    def __repr__(self):
        return f"WaitNode(value={self.value} vale2={self.value2}"

class NowNode:
    def __repr__(self):
        return f"NowNode()"

class WhileNode:
    def __init__(self, exp, value):
        self.exp = exp
        self.value = value
    def __repr__(self):
        return f"WhileNode(exp={self.exp} value={self.value}"

class RepeatNode:
    def __init__(self, value, value2):
        self.value = value
        self.value2 = value2
    def __repr__(self):
        return f"RepeatNode(number={self.value} value={self.value2}"

class ClearNode:
    def __repr__(self):
        return f"ClearNode()"

class MakeNode:
    def __init__(self, var, value):
        self.var = var
        self.value = value
    def __repr__(self):
        return f"MakeNode(var={self.var} value={self.value})"

class BoolNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"BoolNode(value={self.value})"

class MinusNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"MinusNode(value={self.value})"

class PlusNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"PlusNode(value={self.value})"

class NotNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"NotNode(value={self.value})"

class LengthNode:
    def __init__(self, var):
        self.var = var
    def __repr__(self):
        return f"LengthNode(var={self.var})"

class BreakNode:
    def __repr__(self):
        return "BreakNode()"

class ContinueNode:
    def __repr__(self):
        return "ContinueNode()"

class FunctionDefNode:
    def __init__(self, name, para, body):
        self.name = name
        self.para = para
        self.body = body
    def __repr__(self):
        return f"FunctionDefNode(name={self.name} para={self.para} body={self.body})"

class FunctionCallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args
    def __repr__(self):
        return f"FunctionCallNode(name={self.name} args={self.args})"

class ReturnNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"ReturnNode(value={self.value})"

class HexusParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.loop_depth = 0
        self.current_line = 1
        self.builtin_modules = {}
        self._load_type1_modules()

    def _load_type1_modules(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        modules_dir = os.path.join(base_dir, "modules")

        if not os.path.exists(modules_dir):
            os.makedirs(modules_dir)
            return

        for filename in os.listdir(modules_dir):
            if filename.endswith(".py") and not filename.endswith("_ext.py"):
                mod_name = filename[:-3]
                filepath = os.path.join(modules_dir, filename)

                spec = importlib.util.spec_from_file_location(mod_name, filepath)
                py_mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(py_mod)

                for attr_name in dir(py_mod):
                    attr = getattr(py_mod, attr_name)
                    if attr_name.endswith("Parser") and hasattr(attr, "name") and hasattr(attr, "parse"):
                        self.builtin_modules[attr.name] = attr

    def peek(self, offset=0):
        if self.pos + offset <len(self.tokens):
            return self.tokens[self.pos + offset]
        return "EOF", "EOF"

    def consume(self, expected_type):
        token_type, value = self.peek()

        if token_type == expected_type:
            if token_type == "NEWLINE":
                self.current_line += 1
            self.pos += 1
            return value
        else:
            raise SyntaxError(
                f"[Line: {self.current_line}] expected token of type '{expected_type}', "
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
                f"Syntax error: [Line: {self.current_line}] Expected '{expected_value}', but found '{value}'."
            )

    def consume_end_of_statement(self):
        token_type, _ = self.peek()
        if token_type == "NEWLINE":
            self.consume("NEWLINE")
        elif token_type == "EOF":
            pass
        else:
            raise SyntaxError(f"SynaxError: [Line: {self.current_line}] Expected end of line, but found token of type '{token_type}'")

    def parse_value(self):
        token_type, value = self.peek()

        if token_type == "VAR" and value in self.builtin_modules and self.peek(1)[0] == "DOT":
            node = self.parse_builtin_dot_call()

            if getattr(node, "is_expression", True) is False:
                raise SyntaxError(f"SyntaxError: [Line: {self.current_line}] '{value}' command does not return a value and connot be use inside expression command")
            return node
        elif token_type == "INT":
            self.consume("INT")
            value = int(value)
            return NumberNode(value)
        elif token_type == "VAR" and value == "now":
            self.consume("VAR")
            return NowNode()
        elif token_type == "VAR":
            var_name = self.consume("VAR")
            if self.peek()[0] == "LPAREN":
                return self.parse_func_call(var_name)
            return VariableNode(var_name)
        elif token_type == "STRING":
            val = self.consume("STRING")
            val = val.split()
            return StringNode(val)
        elif token_type == "BOOL":
            self.consume("BOOL")
            return BoolNode(value)
        elif token_type == "OP" and value == "-":
            return self.parse_minus()
        elif token_type == "OP" and value == "+":
            return self.parse_plus()
        else:
            raise SyntaxError(f"SyntaxError: [Line: {self.current_line}] Expect number or variable, but found '{token_type}' ('{value}')")

    def parse_vara(self):
        token_type, value = self.peek()
        if token_type == "VAR":
            self.consume("VAR")
            return VariableNode(value)
        raise SyntaxError(f"???")

    def parse_expression(self):

        token_type, value = self.peek()
        if token_type == "VAR" and value == "not":
            self.consume("VAR")
            value = self.parse_value()
            return NotNode(value)
        if token_type == "STRING":
            val = self.consume("STRING")
            val = val.split()
            return StringNode(val)
        left = self.parse_value()

        while True:
            next_type, value = self.peek()

            if next_type == "OP":
                op = self.consume("OP")

                right = self.parse_value()
                left = BinaryOpNode(left, op, right)
            elif (next_type == "OP" and value == "!=") or (next_type == "VAR" and value == "is" and self.peek(1)[1] == "not"):
                self.consume(next_type)
                if self.peek()[1] == "not":
                    self.consume("VAR")
                op = "!="
                right = self.parse_value()
                left = BinaryOpNode(left, op, right)
            elif (next_type == "OP" and value == "==") or (next_type == "VAR" and value == "is"):
                self.consume(next_type)
                op = "=="
                right = self.parse_value()
                left = BinaryOpNode(left, op, right)
            elif next_type == "VAR" and value in ["and", "or"]:
                self.consume("VAR")
                op = value
                right = self.parse_expression()
                left = BinaryOpNode(left, op, right)
            else:
                break
        return left

    def peek_is_list_expression(self):
        if self.peek()[0] == "LSBRACE":
            return True

        if self.peek()[0] in ["STRING", "INT", "VAR"] and self.peek(1)[0] == "COMMA":
            return True

        return False

    def parse_var(self):
        is_list = False
        var_name = self.consume("VAR")

        token_type, value = self.peek()

        if token_type == "OP" and value == "=":
            self.consume("OP")


        elif token_type == "VAR" and value == "is":
            self.consume_value("VAR", "is")

        else:
            raise SyntaxError(f"SyntaxError: [Line: {self.current_line}] Expected '=' or 'is', but found {token_type} ('{value}')")

        is_empty_list = (self.peek()[0] == "LSBRACE" and self.peek(1)[0] == "RSBRACE")

        if is_empty_list or self.peek_is_list_expression():
            is_list = True

            if is_empty_list:
                self.consume("LSBRACE")
                self.consume("RSBRACE")
                expr_value = None
            else:
                expr_value = []

                while self.peek()[0] not in ["NEWLINE", "EOF"]:

                    if self.peek()[0] == "LSBRACE":
                        self.consume("LSBRACE")
                        expr_value.append(self.parse_expression())
                        self.consume("RSBRACE")

                    else:
                        expr_value.append(self.parse_expression())

                    if self.peek()[0] == "COMMA":
                        self.consume("COMMA")
                    else:
                        raise SyntaxError(f"SyntaxError: [Line: {self.current_line}] Expected ',' after list element, but found {self.peek()[0]}")

        else:
            expr_value = self.parse_expression()

        self.consume_end_of_statement()
        return SetVar(var_name, expr_value, is_list)



    def parse_send(self):
        target = "console"
        self.consume("VAR")
        if self.peek()[0] == "VAR" and self.peek()[1] == "length":
            text = self.parse_length()
        else:
            text = self.parse_expression()
        token_type, value = self.peek()
        if token_type == "VAR" and value == "to":
            self.consume_value("VAR", "to")
            target = self.consume("VAR")
        self.consume_end_of_statement()
        return SendCommandNode(text, target)

    def parse_read(self):
        target = "console"
        self.consume("VAR")
        text = self.parse_expression()
        self.consume_value("VAR", "to")
        var = self.consume("VAR")
        token_type, value = self.peek()
        if token_type == "VAR" and value == "from":
            self.consume_value("VAR", "from")
            target = self.consume("VAR")
        self.consume_end_of_statement()
        return ReadCommandNode(text, var, target)

    def parse_stop(self):
        value = None
        self.consume("VAR")
        if self.peek()[0] == "STRING":
            value = self.parse_value()
        self.consume_end_of_statement()
        return StopNode(value)

    def parse_com(self):
        text = []
        self.consume("HASH")
        while self.peek()[0] != "NEWLINE" and self.peek()[0] != "EOF":
            text.append(self.advance())
        self.consume_end_of_statement()
        return ComNode(" ".join(text))

    def parse_if(self):
        self.consume_value("VAR", "if")
        exp = self.parse_expression()
        value = self.parse_block()
        elifv = {}
        while self.peek()[0] == "VAR" and self.peek()[1] == "elif":
            self.consume_value("VAR", "elif")
            elexp = self.parse_expression()
            elvalue = self.parse_block()
            elifv[elexp] = elvalue
            self.consume_end_of_statement()
        value2 = None
        if self.peek()[0] == "VAR" and self.peek()[1] == "else":
            self.consume_value("VAR", "else")
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

    def parse_listadd(self):
        pos = None
        self.consume_value("VAR", "add")
        token_type, value = self.peek(0)
        if token_type == "INT" or token_type == "VAR" or token_type == "STRING":
            value = self.parse_value()
        self.consume_value("VAR", "to")
        is_list = self.parse_vara()
        if self.peek()[0] == "VAR" and self.peek()[1] == "at":
            self.consume_value("VAR", "at")
            if self.peek()[0] == "VAR" and self.peek()[1] == "pos":
                self.consume_value("VAR", "pos")
                if self.peek()[0] == "INT":
                    pos = self.parse_value()
        self.consume_end_of_statement()
        return ListAddNode(is_list, value, pos)


    def parse_listremove(self):
        pos = None
        value = None
        self.consume_value("VAR", "remove")
        token_type, valuee = self.peek(0)
        if token_type == "VAR" and valuee == "pos":
            self.consume_value("VAR", "pos")
            if self.peek()[0] == "INT":
                pos = self.parse_value()
        elif token_type == "INT" or token_type == "VAR" or token_type == "STRING":
            value = self.parse_value()
        self.consume_value("VAR", "from")
        is_list = self.parse_vara()
        return ListRemoveNode(is_list, pos, value)

    def parse_wait(self):
        self.consume_value("VAR", "wait")
        if self.peek()[0] == "INT":
            value = self.parse_value()
            if self.peek()[0] == "VAR" and (self.peek()[1] == "s" or self.peek()[1] == "m" or self.peek()[1] == "h" or self.peek()[1] == "d"):
                value2 = self.parse_value()
                self.consume_end_of_statement()
                return WaitNode(value, value2)
        raise SyntaxError(f"???")

    def parse_while(self):
        self.consume_value("VAR", "while")
        if self.peek()[0] == "INT" or self.peek()[0] == "VAR":
            exp = self.parse_expression()
            self.loop_depth += 1
            value = self.parse_block()
            self.loop_depth -= 1
            self.consume_end_of_statement()
            return WhileNode(exp, value)
        raise SyntaxError(f"???")


    def parse_repeat(self):
        self.consume_value("VAR", "repeat")
        if self.peek()[0] == "INT" or self.peek()[0] == "VAR":
            value = self.parse_value()
            if self.peek()[0] == "VAR" and self.peek()[1] == "times":
                self.consume_value("VAR", "times")
                self.loop_depth += 1
                value2 = self.parse_block()
                self.loop_depth -= 1
                self.consume_end_of_statement()
                return RepeatNode(value, value2)
            else:
                raise SyntaxError(f"SyntaxError: [Line: {self.current_line}] Expected 'times' but found {self.peek()[1]}")
        else:
            raise SyntaxError(f"SyntaxError: [Line: {self.current_line}] Expected number but found {self.peek()[1]}")


    def parse_clear(self):
        self.consume_value("VAR", "clear")
        if self.peek()[0] == "VAR" and self.peek()[1] == "screen":
            self.consume_value("VAR", "screen")
        self.consume_end_of_statement()
        return ClearNode()


    def parse_make(self):
        self.consume_value("VAR", "make")
        if self.peek()[0] == "VAR":
            var = self.consume("VAR")
            if self.peek()[0] == "VAR" and self.peek()[1] == "lower":
                value = "lower"
                self.consume("VAR")
            elif self.peek()[0] == "VAR" and self.peek()[1] == "upper":
                value = "upper"
                self.consume("VAR")
            else:
                raise SyntaxError(f"SyntaxError: [Line: {self.current_line}] Expected lower or upper but found {self.peek()[0]}")
            self.consume_end_of_statement()
            return MakeNode(var, value)
        else:
            raise SyntaxError(f"SyntaxError: [Line: {self.current_line}] Expected VAR but found {self.peek()[0]}")



    def parse_minus(self):
        self.consume("OP")
        if self.peek()[0] == "INT":
            value = self.parse_value()
            return MinusNode(value)
        raise SyntaxError("???")

    def parse_plus(self):
        self.consume("OP")
        if self.peek()[0] == "INT":
            value = self.parse_value()
            return PlusNode(value)
        raise SyntaxError("???")


    def parse_length(self):
        self.consume("VAR")
        if self.peek()[0] == "VAR" and self.peek()[1] == "of":
            self.consume_value("VAR", "of")
            var = self.parse_value()
            return LengthNode(var)
        raise SyntaxError("???")


    def parse_break(self):
        self.consume_value("VAR", "break")
        return BreakNode()


    def parse_continue(self):
        self.consume_value("VAR", "continue")
        return ContinueNode()


    def parse_func(self):
        self.consume_value("VAR", "func")
        func_name = self.consume("VAR")
        self.consume("LPAREN")
        para = []
        if self.peek()[0] != "RPAREN":
            para.append(self.consume("VAR"))
            while self.peek()[0] == "COMMA":
                self.consume("COMMA")
                para.append(self.consume("VAR"))
        self.consume("RPAREN")
        body = self.parse_block()
        self.consume_end_of_statement()
        return FunctionDefNode(func_name, para, body)


    def parse_func_call(self, func_name):
        self.consume("LPAREN")
        args = []
        if self.peek()[0] != "RPAREN":
            args.append(self.parse_expression())
            while self.peek()[0] == "COMMA":
                self.consume("COMMA")
                args.append(self.parse_expression())
        self.consume("RPAREN")
        return FunctionCallNode(func_name, args)


    def parse_return(self):
        self.consume_value("VAR", "return")
        token_type, _ = self.peek()
        if token_type in ["NEWLINE", "EOF", "RBRACE"]:
            value = None
        else:
            value = self.parse_expression()
        self.consume_end_of_statement()
        return ReturnNode(value)


    def parse_builtin_dot_call(self):
        mod_name = self.consume("VAR")
        self.consume("DOT")
        module_class = self.builtin_modules[mod_name]
        return module_class.parse(self)





    def parse_statement(self):
        while self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")

        token_type, value = self.peek()

        if token_type == "VAR" and value in self.builtin_modules and self.peek(1)[0] == "DOT":
            return self.parse_builtin_dot_call()
        elif token_type == "VAR" and value == "send":
            return self.parse_send()
        elif token_type == "VAR" and value == "read":
            return self.parse_read()
        elif token_type == "HASH" and value == "#":
            return self.parse_com()
        elif token_type == "VAR" and value == "if":
            return self.parse_if()
        elif token_type == "VAR" and value == "add":
            return self.parse_listadd()
        elif token_type == "VAR" and value == "remove":
            return self.parse_listremove()
        elif token_type == "VAR" and value == "wait":
            return self.parse_wait()
        elif token_type == "VAR" and value == "while":
            return self.parse_while()
        elif token_type == "VAR" and value == "repeat":
            return self.parse_repeat()
        elif token_type == "VAR" and value == "clear":
            return self.parse_clear()
        elif token_type == "VAR" and value == "make":
            return self.parse_make()
        elif token_type == "VAR" and value == "length":
            return self.parse_length()
        elif token_type == "OP" and value == "-":
            return self.parse_minus()
        elif token_type == "OP" and value == "+":
            return self.parse_plus()
        elif token_type == "VAR" and value == "stop":
            return self.parse_stop()
        elif token_type == "VAR" and value == "func":
            return self.parse_func()
        elif token_type == "VAR" and value == "return":
            return self.parse_return()
        elif token_type == "VAR" and value == "break":
            if self.loop_depth > 0:
                return self.parse_break()
            else:
                raise SyntaxError(f"[LINE: {self.current_line}] You can't use break outside of loop")
        elif token_type == "VAR" and value == "continue":
            if self.loop_depth > 0:
                return self.parse_continue()
            else:
                raise SyntaxError(f"[LINE: {self.current_line}] You can't use continue outside of loop")
        elif token_type == "INT":
            return self.parse_expression()
        elif token_type == "VAR":
            if self.peek(1)[0] == "LPAREN":
                func_name = self.consume("VAR")
                node = self.parse_func_call(func_name)
                self.consume_end_of_statement()
                return node
            next_type, next_value = self.peek(1)
            if (next_type == "OP" and next_value == "=") or (next_type == "VAR" and next_value == "is"):
                return self.parse_var()
            else:
                return self.parse_expression()
        else:
            raise SyntaxError(f"SyntaxError: [Line: {self.current_line}] Unknown start instruction: {token_type} ('{value}')")


    def parse(self):
        program_nodes = []
        while self.peek()[0] != "EOF":
            if self.peek()[0] == "NEWLINE":
                self.consume("NEWLINE")
                continue

            node = self.parse_statement()
            program_nodes.append(node)


        return program_nodes
