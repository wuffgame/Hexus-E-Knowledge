from datetime import datetime, timezone, timedelta
import types

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

class TimeDayNode:
    is_expression = True
    def __repr__(self):
        return "TimeDayNode()"

class TimeMonthNode:
    is_expression = True
    def __repr__(self):
        return "TimeMonthNode()"

class TimeYearNode:
    is_expression = True
    def __repr__(self):
        return "TimeYearNode()"


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
        elif token_type == "VAR" and value == "day":
            parser.consume_value("VAR", "day")
            return TimeParser.parse_day(parser)
        elif token_type == "VAR" and value == "month":
            parser.consume_value("VAR", "month")
            return TimeParser.parse_month(parser)
        elif token_type == "VAR" and value == "year":
            parser.consume_value("VAR", "year")
            return TimeParser.parse_year(parser)
        elif token_type == "VAR" and value == "get":
            parser.consume_value("VAR", "get")
            return TimeParser.parse_time(parser)
        raise SyntaxError(f"SyntaxError [time module]: Unknown command 'time.{value}'")

    @staticmethod
    def parse_hour(parser):
        return TimeHourNode()

    @staticmethod
    def parse_minute(parser):
        return TimeMinuteNode()

    @staticmethod
    def parse_second(parser):
        return TimeSecNode()

    @staticmethod
    def parse_day(parser):
        return TimeDayNode()

    @staticmethod
    def parse_month(parser):
        return TimeMonthNode()

    @staticmethod
    def parse_year(parser):
        return TimeYearNode()

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
            _ = node, self
            return datetime.now().strftime("%H")

        def visit_TimeMinuteNode(self, node):
            _ = node, self
            return datetime.now().strftime("%M")

        def visit_TimeSecNode(self, node):
            _ = node, self
            return datetime.now().strftime("%S")

        def visit_TimeDayNode(self, node):
            _ = node, self
            return datetime.now().strftime("%d")

        def visit_TimeMonthNode(self, node):
            _ = node, self
            return datetime.now().strftime("%m")

        def visit_TimeYearNode(self, node):
            _ = node, self
            return datetime.now().strftime("%Y")

        def visit_TimeTimeNode(self, node):
            value = self.visit(node.value)
            return datetime.now().strftime(value)

        def visit_TimeUTCNode(self, node):
            tz_val = self.visit(node.value_node)
            if isinstance(tz_val, _UTC):
                tz_val = timezone.utc
            elif isinstance(tz_val, int):
                tz_val = timezone(timedelta(hours=tz_val))

            return datetime.now(tz_val).strftime("%Y-%m-%d %H:%M:%S")

        handlers = {
            "visit_TimeHourNode": visit_TimeHourNode,
            "visit_TimeMinuteNode": visit_TimeMinuteNode,
            "visit_TimeSecNode": visit_TimeSecNode,
            "visit_TimeDayNode": visit_TimeDayNode,
            "visit_TimeMonthNode": visit_TimeMonthNode,
            "visit_TimeYearNode": visit_TimeYearNode,
            "visit_TimeTimeNode": visit_TimeTimeNode,
            "visit_TimeUTCNode": visit_TimeUTCNode,
        }

        for name, func in handlers.items():
            setattr(interpreter, name, types.MethodType(func, interpreter))
