const editor = document.getElementById("editor")
const output = document.getElementById("output")
const runBtn = document.getElementById("run-btn")
const clearBtn = document.getElementById("clear-btn")
const statusDot = document.getElementById("status-dot")
const statusText = document.getElementById("status-text")

window.hexusPrompt = function (promptText) {
    const value = window.prompt(promptText || "Type value:");
    return value === null ? "" : value
}

const python_file = ["main.py", "lexer.py", "parser.py", "interpreter.py"];
const python_folder = "hexus-lang";

function setStatus(state) {
    statusText.textContent = state
    statusDot.style.backgroundColor =
        state === "error" ? "#c0392b" :
        state === "launching" || state === "loading..." ? "#e8b923" : "#7a6218"
}

let pyodideInstance = null;

async function initPyodide() {
    setStatus("loading...");
    runBtn.disabled == true;

    const pyodide = await loadPyodide();

    for (const name of python_file) {
        const ans = await fetch(`${python_folder}/${name}`);
        if (!ans.ok) {
            throw new Error(`Not found: ${python_folder}/${name}`);
        }
        const text = await ans.text();
        pyodide.FS.writeFile(name, text);
    }

    pyodide.runPython(`
import sys
if '.' not in sys.path:
    sys.path.insert(0, '.')
`);

    pyodide.runPython(`
import builtins
import js
 
def _hexus_input(prompt=''):
    value = js.hexusPrompt(str(prompt))
    return '' if value is None else value
 
builtins.input = _hexus_input
`);

    runBtn.disabled = false;
    setStatus("ready");
    return pyodide
}

const pyodideReady = initPyodide().catch((err) => {
    setStatus("Error")
    output.textContent = "# Error while loading Pyodide:\n" + err.message;
    throw err;
});

runBtn.addEventListener("click", async () => {
    setStatus("launching");
    output.textContent = "";

    try {
        const pyodide = await pyodideReady;

        let logs = "";
        pyodide.setStdout({ batched: (s) => { logs += s + '\n'; } });
        pyodide.setStderr({ batched: (s) => { logs += s + '\n'; } });

        pyodide.globals.set("user_code", editor.value);

        const result = await pyodide.runPythonAsync(`
import importlib
import main
importlib.reload(main)
main.start(user_code)
    `);

    const final_text = logs + (result ?? '');
    output.textContent = final_text.trim() || '# The program did not return any result.';
    setStatus("ready");
    } catch (err) {
        output.textContent = "runtime error:\n" + err.message;
        setStatus("error")
    }
});

clearBtn.addEventListener("click", () => {
    editor.value = ""
    output.textContent = "# here result";
    setStatus("ready");
})

