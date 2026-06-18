import re

token_pattern = [
        ("INT", r"\d+"),
        ("PLUS", r"\+"),
        ("MINUS", r"\-"),
        ("MUL", r"\*"),
        ("DIV", r"\/"),
        ("SPACE", r"\s+"),
    ]

def tokenizer(text, definition):
    patter = []
    for name, regex in definition:
        patter.append(f"(?P<{name}>{regex})")

    full_regex = "|".join(patter)

    tokens = []

    for match in re.finditer(full_regex, text):
        kind = match.lastgroup
        value = match.group()

        tokens.append((kind, value))

    return tokens

tekst = "12+5-432*13/5"
print(tokenizer(tekst, token_pattern))