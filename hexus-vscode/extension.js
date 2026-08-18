const vscode = require("vscode");

function activate(context) {
    let disposable = vscode.commands.registerCommand("hexus.run", function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.ShowErrorMessage("No active file to run!")
            return;
        }
        const filePath = editor.document.fileName;
        let terminal = vscode.window.terminals.find(t => t.name === "Hexus");
        if (!terminal) {
            terminal = vscode.window.createTerminal("Hexus");
        }
        terminal.show();
        terminal.sendText(`hexus '${filePath}'`);
    });
    context.subscriptions.push(disposable);
}

function deactive() {}

module.exports = {
    activate,
    deactive
}