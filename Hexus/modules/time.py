from datetime import datetime, timezone, timedelta

class _UTC:
    def __add__(self, h):
        return timezone(timedelta(hours=int(h)))

    def __sub__(self, h):
        return timezone(timedelta(hours=-int(h)))

    def __repr__(self):
        return "UTC"


UTC = _UTC()



class TimeHourNode:
    is_expression = True
    def __repr__(self):
        return "TimeHourNode()"


class TimeMinuteNode:
    is_expression = True
    def __repr__(self):
        return "TimeMinuteNode()"


class TimeSecNode:
    is_expression = True
    def __repr__(self):
        return "TimeSecNode()"


class TimeTimeNode:
    is_expression = True
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"TimeTimeNode(value={self.value})"


class TimeUTCNode:
    is_expression = True
    def __init__(self, value_node):
        self.value_node = value_node
    def __repr__(self):
        return f"TimeUTCNode(value={self.value_node})"



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
            else:
                expr_node = parser.parse_expression()
                return TimeUTCNode(expr_node)
        else:
            raise SyntaxError("SyntaxError [time module]: Expected 'time' after 'get'")



class TimeInterpreter:
    @staticmethod
    def register_handlers(interpreter):
        interpreter.env.set("UTC", UTC)

        def visit_TimeHourNode(self, node):
            return datetime.now().strftime("%H")

        def visit_TimeMinuteNode(self, node):
            return datetime.now().strftime("%M")

        def visit_TimeSecNode(self, node):
            return datetime.now().strftime("%S")

        def visit_TimeTimeNode(self, node):
            value = interpreter.visit(node.value)
            return datetime.now().strftime(value)

        def visit_TimeUTCNode(self, node):
            tz_val = interpreter.visit(node.value_node)
            if isinstance(tz_val, _UTC):
                tz_val = timezone.utc
            elif isinstance(tz_val, int):
                tz_val = timezone(timedelta(hours=tz_val))

            return datetime.now(tz_val).strftime("%Y-%m-%d %H:%M:%S")

        setattr(interpreter.__class__, "visit_TimeHourNode", visit_TimeHourNode)
        setattr(interpreter.__class__, "visit_TimeMinuteNode", visit_TimeMinuteNode)
        setattr(interpreter.__class__, "visit_TimeSecNode", visit_TimeSecNode)
        setattr(interpreter.__class__, "visit_TimeTimeNode", visit_TimeTimeNode)
        setattr(interpreter.__class__, "visit_TimeUTCNode", visit_TimeUTCNode)