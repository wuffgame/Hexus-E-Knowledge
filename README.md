# Hexus-E-Knowledge

A programming language designed to make code easy to read and write.

Try Hexus in the browser -> [Playground](https://hexus-lang.dev/Playground)

You can find the homepage by visiting [https://hexus-lang.dev](https://hexus-lang.dev)

---

## What is it?

Hexus (otherwise known as E-Knowledge) is a high-level, easy-to-learn programming language designed to read almost like plain English. It comes with a fully browser-based Playground (powered by Pyodide - Python in WebAssembly), a Visual Studio Code extension, and a growing standard library of modules. No installation is required - open the Playground and start coding.

---

## Why this project?

I'm 16, I joined Hack Club, and I've always wanted to build something BIG and something that matters, not just another todo app or Discord bot. A lot of people think that making your own programming language is impossible, or something only "real" programmers do.

I started writing Hexus as an innocent project for Macondo ysws. I wanted to create something that:

- Actually works (not just a parser that crashes on the second line)
- Runs in the browser so anyone can try it instantly
- Is modular and extensible - you can add new features by dropping a .py or .he file into the modules folder
- Feels beginner-friendly - minimal special characters, readable syntax, clear error messages

---

## Current limitations

Since this project is currently in early alpha (v0.1.1) and built by one teenager in their spare time, there are a few limitations:

- The Playground runs entirely client-side - your code never leaves your browser. There is no backend server for execution, which means no privacy concerns, but also no persistent storage.
- Pyodide has a ~15 MB initial download - the first load may take a few seconds. After that, it's cached by the browser.
- The language is not yet production-ready - while it supports variables, functions, loops, lists, conditionals, string interpolation, modules, and file I/O, there may be edge cases that crash the interpreter.
- The VS Code extension provides syntax highlighting (.he files), but does not yet include a language server or debugger.

---

## Features

- Dynamic typing - Variables can hold numbers, strings, booleans, or lists - no type declarations needed
- String interpolation - "`Hello {name}, you are {age} years old`" - expressions inside strings are evaluated
- List operations - `add`, `remove`, `length of`, `pos of`
- Conditionals - `if/elif/else` with comparison and logical operators (`and`, `or`, `not`)
- Loops - `while`, `repeat N times`, `for each in list`, `for x from y to z`
- Functions - `func` with proper lexical scoping
- Modules - Dynamic plugin system - drop a `.py` or `.he` file into modules/ and it's automatically loaded
- @syntax declarations - Modules can define custom syntax for the language parser
- File I/O - `open`, `read`, `readline`, `write`, `append`, `close`
- Time utilities - `hour`, `minute`, `second`, `day`, `month`, `year`, `get time`, `UTC`
- Block comments - `// ... //` - multi-line comments
- Browser Playground - Full Pyodide-based IDE in the browser with output panel
- VS Code extension - Syntax highlighting for `.he` files

---

## Installation

### Option 1: Playground (No Installation)

Just open [https://hexus-lang.dev/Playground/](https://hexus-lang.dev/Playground/) in your browser. Type code, hit RUN and see the output. That's it.

The Playground supports a single file - perfect for experimenting, learning, or testing small scripts.

Note: The Playground may not always be on the latest version. For the bleeding edge, install locally.

### Option 2: Local Installation (via pip)

**Requirements:**

- Python 3.8 or higher
- pip

**Guide:**

`pip install hexus-lang`

Then create a file with the `.he` extension:

`send "Hello World!!!"`

And run it:

`hexus myfile.he`

### Option 3: VS Code Extension

1. Install Hexus from Option 2 Guide
2. Open Visual Studio Code
3. Go to the Extensions tab (Ctrl+Shift+X)
4. Search for "Hexus"
5. Install the extension by wuff (me c: )
6. Restart VS Code
7. Open any `.he` file - syntax highlighting will activate automatically

---

## Quick Start

### Hello World

`send "Hello World!!!"`

### Variables and Math

```
x is 10
y is 20
sum is x + y
send "The sum of {x} and {y} is {sum}"
```

### Conditional Logic

```
age is 16
if age >= 18 {
    send "You are an adult"
}
else {
    send "You are a minor"
}        
```

For more go to [https://hexus-lang.dev/Docs](https://hexus-lang.dev/Docs)

---

## AI Usage

I used AI to help with:

- Providing library suggestions
- Help with style.css
- Help fixing errors I didn't understand

I wrote the rest of the language's code entirely myself (for now, maybe someone will be tempted to do a pull request).

---

## Credits

Thanks Hack Club and Macondo for giving me the motivation to actually build this instead of just adding it to my "someday" list.

---

## License

The project is licensed under the **GNU General Public License v3.0**. See the LICENSE file for details.

---

### Contact

If you notice any errors, have an idea, or just want to say hi:

- Discord: _anik2010_
- Email: kacper5555544444@gmail.com
- Github Issues: [https://github.com/wuffgame/Hexus-E-Knowledge/issues](https://github.com/wuffgame/Hexus-E-Knowledge/issues)
- Hack Club Slack: wuff

---

Happy coding with Hexus!!!

### Make programming easier!!!