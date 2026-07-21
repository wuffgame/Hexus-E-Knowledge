from interpreter import HexusInterpreter
from parser import HexusParser
from lexer import tokenizer_tokens

def start(source_code: str) -> str:
    token_list = tokenizer_tokens(source_code)
    clear_tokens = [t for t in token_list if t[0] != "SKIP"]

    try:
        parser = HexusParser(clear_tokens)
        program_tree = parser.parse()

        interpreter = HexusInterpreter()
        result = interpreter.interpret(program_tree)

        return str(result) if result is not None else ""

    except SyntaxError as e:
        return f"Błąd składni: {e}"


def main():
    file_name = "test.he"
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"File {file_name} not found!!!")
        return

    print(uruchom(source_code))


if __name__ == "__main__":
    main()