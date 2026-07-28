from datetime import datetime

class TimeHourNode:
    is_expression = True
    def __repr__(self):
        return f"TimeHourNode()"

class TimeMinuteNode:
    is_expression = True
    def __repr__(self):
        return f"TimeMinuteNode()"

class TimeSecNode:
    is_expression = True
    def __repr__(self):
        return f"TimeSecNode()"

class TimeTimeNode:
    is_expression = True
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"TimeTimeNode(value={self.value})"


class TimeParser:
    name = "time"

    @staticmethod
    def parse(parser):
        token_type, value = parser.peek()
        if token_type == "VAR" and value == "hour":
            parser.consume_value("VAR", "hour")
            return TimeParser.parse_hour(parser)
        elif token_type == "VAR" and value == "minute":
            parser.consume_value("VAR", "minute")
            return TimeParser.parse_minute(parser)
        elif token_type == "VAR" and value == "second":
            parser.consume_value("VAR", "second")
            return TimeParser.parse_second(parser)
        elif token_type == "VAR" and value == "get":
            parser.consume_value("VAR", "get")
            return TimeParser.parse_time(parser)
        raise SyntaxError(f"SyntaxError [time module]: Unknown command 'time.{value}'")

    @staticmethod
    def parse_hour(parser):
        parser.consume_end_of_statement()
        return TimeHourNode()

    @staticmethod
    def parse_minute(parser):
        parser.consume_end_of_statement()
        return TimeMinuteNode()

    @staticmethod
    def parse_second(parser):
        parser.consume_end_of_statement()
        return TimeSecNode()

    @staticmethod
    def parse_time(parser):
        if parser.peek()[0] == "VAR" and parser.peek()[1] == "time":
            parser.consume_value("VAR", "time")
            if parser.peek()[0] == "STRING":
                value = parser.parse_value()
                return TimeTimeNode(value)


class TimeInterpreter:
    @staticmethod
    def register_handlers(interpreter):

        def visit_TimeHourNode(self, node):
            _ = self, node
            hour = datetime.now().strftime("%H")
            return hour

        def visit_TimeMinuteNode(self, node):
            _ = self, node
            minute = datetime.now().strftime("%M")
            return minute

        def visit_TimeSecNode(self, node):
            _ = self, node
            sec = datetime.now().strftime("%S")
            return sec

        def visit_TimeTimeNode(self, node):
            _ = self
            value = interpreter.visit(node.value)
            return datetime.now().strftime(value)

        setattr(interpreter.__class__, "visit_TimeHourNode", visit_TimeHourNode)
        setattr(interpreter.__class__, "visit_TimeMinuteNode", visit_TimeMinuteNode)
        setattr(interpreter.__class__, "visit_TimeSecNode", visit_TimeSecNode)
        setattr(interpreter.__class__, "visit_TimeTimeNode", visit_TimeTimeNode)