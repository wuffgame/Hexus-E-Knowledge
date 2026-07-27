class TimeHourNode:
    is_expression = True
    def __repr__(self):
        return f"TimeHourNode()"


class TimeParser:
    name = "time"

    @staticmethod
    def parse(parser):
        token_type, value = parser.peek()
        if token_type == "VAR" and value == "hour":
            parser.consume_value("VAR", "hour")
            return TimeParser.parse_hour(parser)
        raise SyntaxError(f"SyntaxError [time module]: Unknown command 'time.{value}'")

    @staticmethod
    def parse_hour(parser):
        parser.consume_end_of_statement()
        return TimeHourNode()


class TimeInterpreter:
    @staticmethod
    def register_handlers(interpreter):

        def visit_TimeHourNode(self, node):
            import time
            hour = time.strftime("%H")
            return hour

        setattr(interpreter.__class__, "visit_TimeHourNode", visit_TimeHourNode)