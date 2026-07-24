import re

token_pattern = [
        ("HASH", r"#"),
        ("INT", r"\d+"),
        ("BOOL", r"\b(True|False)\b"),
        ("OP", r">=|<=|==|!=|[+\-=*/><]"),
        ("STRING", r'"[^"\\]*(?:\\.[^"\\]*)*"'),
        ("VAR", r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ("LBRACE", r'\{'),
        ("RBRACE", r'\}'),
        ("LSBRACE", r"\["),
        ("RSBRACE", r"\]"),
        ("SKIP", r'[ \t]+'),
        ("NEWLINE", r'\n'),
        ("COMMA", r"\,")
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

def tokenizer_tokens(text):
    tokens = tokenizer(text, token_pattern)
    return tokens