import types
from typing import Any


class FileOpenNode:
    is_expression = False
    def __init__(self, value, var):
        self.value = value
        self.var = var
    def __repr__(self):
        return f"FileOpenNode(value={self.value}, var={self.var})"


class FileReadNode:
    is_expression = False
    def __init__(self, file, var):
        self.file = file
        self.var = var
    def __repr__(self):
        return f"FileReadNode(file={self.file}, var={self.var})"

class FileReadLineNode:
    is_expression = False
    def __init__(self, file, var):
        self.file = file
        self.var = var
    def __repr__(self):
        return f"FileReadLineNode(file={self.file}, var={self.var})"

class FileWriteNode:
    def __init__(self, value, file):
        self.value = value
        self.file = file
    def __repr__(self):
        return f"FileWriteNode(value={self.value}, file={self.file})"

class FileCloseNode:
    def __init__(self, file):
        self.file = file
    def __repr__(self):
        return f"FileCloseNode(file={self.file})"

class FileParser:
    name = "file"

    @staticmethod
    def parse(parser):
        token_type, value = parser.peek()
        if token_type == "VAR" and value == "open":
            parser.consume_value("VAR", "open")
            return FileParser.parse_open(parser)
        elif token_type == "VAR" and value == "read":
            parser.consume_value("VAR", "read")
            return FileParser.parse_read(parser)
        elif token_type == "VAR" and value == "readline":
            parser.consume_value("VAR", "readline")
            return FileParser.parse_readline(parser)
        elif token_type == "VAR" and value == "write":
            parser.consume_value("VAR", "write")
            return FileParser.parse_write(parser)
        elif token_type == "VAR" and value == "close":
            parser.consume_value("VAR", "close")
            return FileParser.parse_close(parser)


    @staticmethod
    def parse_open(parser):
        value = parser.parse_value()
        parser.consume_value("VAR", "as")
        if parser.peek()[0] == "VAR":
            var = parser.parse_value()
            return FileOpenNode(value, var)
        raise SyntaxError("???")

    @staticmethod
    def parse_read(parser):
        if parser.peek()[0] == "VAR":
            file = parser.parse_value()
            parser.consume_value("VAR", "into")
            if parser.peek()[0] == "VAR":
                var = parser.parse_value()
                return FileReadNode(file, var)
        raise SyntaxError("???")

    @staticmethod
    def parse_readline(parser):
        if parser.peek()[0] == "VAR":
            file = parser.parse_value()
            parser.consume_value("VAR", "into")
            if parser.peek()[0] == "VAR":
                var = parser.parse_value()
                return FileReadLineNode(file, var)
        raise SyntaxError("???")

    @staticmethod
    def parse_write(parser):
        value = parser.parse_value()
        parser.consume_value("VAR", "to")
        if parser.peek()[0] == "VAR":
            file = parser.parse_value()
            return FileWriteNode(value, file)
        raise SyntaxError("???")

    @staticmethod
    def parse_close(parser):
        if parser.peek()[0] == "VAR":
            file = parser.parse_value()
            return FileCloseNode(file)
        raise SyntaxError("???")







class FileInterpreter:
    @staticmethod
    def register_handlers(interpreter):

        def visit_FileOpenNode(self, node):
            file_name = self.visit(node.value) if hasattr(node.value, "value") else node.value
            var_name = node.var.name if hasattr(node.var, "name") else str(node.var)
            try:
                file_obj = open(file_name, "r+", encoding="utf-8")
            except FileNotFoundError:
                file_obj = open(file_name, "w+", encoding="utf-8")
            self.env.set(var_name, file_obj)

        def visit_FileReadNode(self, node):
            file = self.visit(node.file)
            var = node.var.name
            file_read = file.read()
            self.env.set(var, file_read)

        def visit_FileReadLineNode(self, node):
            file = self.visit(node.file)
            var = node.var.name
            line = file.readline()
            self.env.set(var, line)

        def visit_FileWriteNode(self, node):
            file = self.visit(node.file)
            value = self.visit(node.value)
            file.seek(0)
            file.truncate(0)
            file.write(value)

        def visit_FileCloseNode(self, node):
            file = self.visit(node.file)
            file.close()


        handlers = {
            "visit_FileOpenNode": visit_FileOpenNode,
            "visit_FileReadNode": visit_FileReadNode,
            "visit_FileReadLineNode": visit_FileReadLineNode,
            "visit_FileWriteNode": visit_FileWriteNode,
            "visit_FileCloseNode": visit_FileCloseNode,
        }

        for name, func in handlers.items():
            setattr(interpreter, name, types.MethodType(func, interpreter))
