import tkinter as tk
from tkinter import simpledialog

variables = {}

# -----------------------------
# 50 custom Lexicon statements
# -----------------------------
statements = [
    "say", "ask", "set", "get", "add", "sub", "show", "hide", "loop", "wait",
    "clear", "alert", "combine", "replace", "length", "random", "color", "background",
    "music", "sound", "mute", "unmute", "notify", "time", "date"
]

# -----------------------------
# 50 custom Lexicon functions
# -----------------------------
functions = [
    "repeat", "call", "pause", "resume", "refresh", "display", "animate", "vibrate",
    "slide", "grow", "shrink", "fade", "rotate", "shake", "connect", "disconnect",
    "encrypt", "decrypt", "filter", "sort", "reverse", "unique", "sum", "avg", "max"
]

# -----------------------------
# Lexicon Interpreter
# -----------------------------
def execute_line(line, all_lines=None, index=0):
    stripped = line.strip()

    # repeat block
    if stripped.startswith("repeat"):
        try:
            times = int(stripped.split()[1])
        except:
            times = 1
        nested = []
        i = index + 1
        while i < len(all_lines):
            next_line = all_lines[i]
            if len(next_line) - len(next_line.lstrip()) <= len(line) - len(stripped):
                break
            nested.append(next_line)
            i += 1
        for _ in range(times):
            for nl in nested:
                execute_line(nl, all_lines, index)
        return len(nested)

    # ask "question" as var
    elif stripped.startswith("ask "):
        parts = stripped.split(" as ")
        if len(parts) == 2:
            question = parts[0][4:].strip().strip('"')
            var_name = parts[1].strip()
        else:
            question = stripped[4:].strip().strip('"')
            var_name = "_"

        # Show question in output
        output_text.insert(tk.END, f"{question}?\n")
        output_text.see(tk.END)

        # Pop up dialog for user input
        user_input = simpledialog.askstring("Lexicon Input", question)
        if user_input is None:
            user_input = ""

        # Store silently
        variables[var_name] = user_input
        return 0

    # say "message"
    elif stripped.startswith("say "):
        text = stripped[4:].strip().strip('"')
        for var_name, value in variables.items():
            text = text.replace(f"[{var_name}]", value)
        output_text.insert(tk.END, f"{text}\n")
        output_text.see(tk.END)
        return 0

    # set var = value
    elif stripped.startswith("set "):
        try:
            parts = stripped[4:].split("=")
            var_name = parts[0].strip()
            value = parts[1].strip().strip('"')
            variables[var_name] = value
        except:
            output_text.insert(tk.END, "[Error: invalid set statement]\n")
        return 0

    # add / sub
    elif stripped.startswith("add "):
        try:
            parts = stripped.split()
            var_name = parts[1]
            amount = int(parts[2])
            variables[var_name] = str(int(variables.get(var_name, 0)) + amount)
        except:
            output_text.insert(tk.END, "[Error: invalid add statement]\n")
        return 0

    elif stripped.startswith("sub "):
        try:
            parts = stripped.split()
            var_name = parts[1]
            amount = int(parts[2])
            variables[var_name] = str(int(variables.get(var_name, 0)) - amount)
        except:
            output_text.insert(tk.END, "[Error: invalid sub statement]\n")
        return 0

    # built-in statements
    elif stripped in statements:
        output_text.insert(tk.END, f"[Executed statement: {stripped}]\n")
        output_text.see(tk.END)
        return 0

    # built-in functions
    elif stripped in functions:
        output_text.insert(tk.END, f"[Executed function: {stripped}]\n")
        output_text.see(tk.END)
        return 0

    # unknown command
    else:
        output_text.insert(tk.END, f"[Unknown command: {stripped}]\n")
        output_text.see(tk.END)
        return 0

# -----------------------------
# Run Lexicon Code
# -----------------------------
def run_lex_code(code):
    lines = code.splitlines()
    i = 0
    while i < len(lines):
        skip = execute_line(lines[i], lines, i)
        i += skip + 1

def run_code(event=None):
    output_text.delete("1.0", tk.END)
    code = code_text.get("1.0", tk.END)
    run_lex_code(code)

# -----------------------------
# GUI
# -----------------------------
root = tk.Tk()
root.title("Lexicon IDE — Shift+Enter = Run 🔥")

code_text = tk.Text(root, height=20, width=100)
code_text.pack()

# key bindings
def on_key(event):
    if event.state & 0x0001 and event.keysym == "Return":  # Shift + Enter
        run_code()
        return "break"  # stop newline
    # normal Enter makes new line
    elif event.keysym == "Return":
        code_text.insert(tk.INSERT, "\n")
        return "break"

code_text.bind("<KeyPress>", on_key)

run_button = tk.Button(root, text="Run (Shift + Enter)", command=run_code)
run_button.pack(pady=5)

output_text = tk.Text(root, height=15, width=100, bg="#f0f0f0")
output_text.pack()

root.mainloop()
