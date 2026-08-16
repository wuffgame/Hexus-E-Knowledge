import types


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
            parser.consume_value("VAR")
            return FileParser.parse_readline(parser)


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


        handlers = {
            "visit_FileOpenNode": visit_FileOpenNode,
            "visit_FileReadNode": visit_FileReadNode,
        }

        for name, func in handlers.items():
            setattr(interpreter, name, types.MethodType(func, interpreter))
