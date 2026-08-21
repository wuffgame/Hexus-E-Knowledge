const vscode = require("vscode");
const path = require("path");

function activate(context) {
    let disposable = vscode.commands.registerCommand("hexus.run", function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.ShowErrorMessage("No active file to run!")
            return;
        }
        const filePath = editor.document.fileName;
        const fileDirectory = path.dirname(filePath);
        const hexusCommand = vscode.workspace
            .getConfiguration("hexus")
            .get("executable", "hexus");
        let terminal = vscode.window.terminals.find(t => t.name === "Hexus");
        if (!terminal) {
            terminal = vscode.window.createTerminal("Hexus");
        }
        terminal.show();
        // Run from the source file's directory so local imports work even
        // when VS Code opened the workspace somewhere else.
        terminal.sendText(`cd "${fileDirectory}" && "${hexusCommand}" "${filePath}"`);
    });
    context.subscriptions.push(disposable);
}

function deactive() {}

module.exports = {
    activate,
    deactive
}
