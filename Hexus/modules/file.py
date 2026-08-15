
class FileParser:
    name = "file"

    @staticmethod
    def parse(parser):
        token_type, value = parser.peek()
        if token_type == "open":
            parser.consume_value("VAR", "open")
            return FileParser.parse_open()


    @staticmethod
    def parse_open(parser):
        pass

class FileInterpreter:
    pass