import sys
import os
from Hexus.lexer import tokenizer_tokens
from Hexus.parser import HexusParser
from Hexus.interpreter import HexusInterpreter


def main():
    if len(sys.argv) < 2:
        print("Hexus Programming Language")
        print("Use: hexus <file.he>")
        sys.exit(1)

    file_name = sys.argv[1]

    if file_name in ["--help", "-h"]:
        print("Hexus Programming Language CLI")
        print("Use: hexus <file.he>")
        sys.exit(0)

    if not os.path.exists(file_name):
        print(f"Error: File '{file_name}' does not exist!")
        sys.exit(1)

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            source_code = file.read()
    except Exception as e:
        print(f"Error while openning file: {e}")
        sys.exit(1)

    try:
        token_list = tokenizer_tokens(source_code)
        clear_tokens = [t for t in token_list if t[0] != "SKIP"]

        parser = HexusParser(clear_tokens)
        program_tree = parser.parse()

        interpreter = HexusInterpreter()
        interpreter.interpret(program_tree)

    except SyntaxError as e:
        print(f"\n{e}")
        sys.exit(1)
    except NameError as e:
        print(f"\n\n{e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nThe program's operation was interrupted (Ctrl+C).")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error:\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
