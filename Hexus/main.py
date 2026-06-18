import sys

filename = sys.argv[1]

with open(filename, "r", encoding="utf-8") as f:
    code = f.read()
print(code)