import tkinter as tk
from tkinter import scrolledtext, PanedWindow, messagebox
import subprocess
import sys
import os
import threading

class SapphireIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("💎 Sapphire Studio v2.4")
        self.root.geometry("1100x700")
        self.process = None
        self.current_file = "Untitled.sp"
        
        # --- 1. Top Toolbar ---
        self.toolbar = tk.Frame(root, bg="#2d2d2d", height=40)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # VERSION SELECTOR
        tk.Label(self.toolbar, text="Version:", bg="#2d2d2d", fg="#aaaaaa").pack(side=tk.LEFT, padx=(10, 2))
        self.ver_entry = tk.Entry(self.toolbar, width=5, bg="#3c3c3c", fg="white", insertbackground="white", bd=0)
        
        detected_ver = self.detect_version()
        self.ver_entry.insert(0, detected_ver) 
        self.ver_entry.pack(side=tk.LEFT, padx=2)

        # Buttons
        self.new_btn = tk.Button(self.toolbar, text="+ NEW", command=self.new_file, bg="#9b59b6", fg="white", font=("Segoe UI", 9, "bold"), padx=10, pady=2, bd=0, cursor="hand2")
        self.new_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.run_btn = tk.Button(self.toolbar, text="▶ RUN", command=self.run_code, bg="#2ecc71", fg="white", font=("Segoe UI", 9, "bold"), padx=10, pady=2, bd=0, cursor="hand2")
        self.run_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_btn = tk.Button(self.toolbar, text="■ STOP", command=self.stop_code, bg="#e74c3c", fg="white", font=("Segoe UI", 9, "bold"), padx=10, pady=2, bd=0, cursor="hand2", state="disabled")
        self.stop_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_btn = tk.Button(self.toolbar, text="💾 SAVE", command=self.save_file, bg="#3498db", fg="white", font=("Segoe UI", 9, "bold"), padx=10, pady=2, bd=0, cursor="hand2")
        self.save_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.status_label = tk.Label(self.toolbar, text="Ready", bg="#2d2d2d", fg="white", font=("Consolas", 9))
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # --- 2. Layout ---
        self.panes = PanedWindow(root, orient=tk.HORIZONTAL, bg="#1e1e1e", sashwidth=6, sashrelief=tk.RAISED)
        self.panes.pack(fill=tk.BOTH, expand=True)

        self.editor = scrolledtext.ScrolledText(self.panes, font=("Consolas", 12), bg="#252526", fg="#d4d4d4", insertbackground="white", undo=True)
        self.panes.add(self.editor, minsize=300)

        self.console = scrolledtext.ScrolledText(self.panes, state='disabled', font=("Consolas", 11), bg="#000000", fg="#00ff00")
        self.panes.add(self.console, minsize=200)

        # Load Welcome Code on Start
        self.load_welcome_code()

    def detect_version(self):
        files = [f for f in os.listdir('.') if f.startswith('Sapphire') and f.endswith('.py') and f != 'SapphireStudio.py']
        if not files: return "19" # Default to latest version
        latest = sorted(files, reverse=True)[0]
        return latest.replace('Sapphire', '').replace('.py', '')

    def load_welcome_code(self):
        welcome = """// 💎 Welcome to Sapphire v1.9
setup {
    var str(greeting){"Hello, Sapphire Developer!"}
    println(var str greeting)
}

main {
    println("System is active and running.")
    exit_game() // Stops the program after one loop
}
"""
        self.editor.insert("1.0", welcome)

    def new_file(self):
        if messagebox.askyesno("New File", "Discard current code and start fresh?"):
            self.editor.delete("1.0", tk.END)
            template = "setup {\n    \n}\n\nmain {\n    \n}"
            self.editor.insert("1.0", template)
            self.status_label.config(text="New Template Loaded", fg="#9b59b6")

    def save_file(self):
        self.current_file = "main.sp" 
        with open(self.current_file, "w", encoding='utf-8') as f:
            f.write(self.editor.get("1.0", tk.END))
        self.root.title(f"Saved as {self.current_file} - Sapphire Studio")
        self.status_label.config(text=f"Saved {self.current_file}", fg="#3498db")

    def log_output(self, text):
        self.console.config(state='normal')
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.config(state='disabled')

    def run_code(self):
        ver = self.ver_entry.get().strip()
        interpreter_file = f"Sapphire{ver}.py"

        if not os.path.exists(interpreter_file):
            messagebox.showerror("Error", f"Missing: {interpreter_file}")
            return

        self.status_label.config(text="Running...", fg="yellow")
        self.stop_btn.config(state="normal")
        self.run_btn.config(state="disabled")
        
        self.console.config(state='normal')
        self.console.delete("1.0", tk.END)
        self.console.config(state='disabled')

        with open("temp_run.sp", "w", encoding='utf-8') as f:
            f.write(self.editor.get("1.0", tk.END))

        thread = threading.Thread(target=self.execute_process, args=(interpreter_file,))
        thread.daemon = True
        thread.start()

    def stop_code(self):
        if self.process:
            if os.name == 'nt':
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])
            else:
                self.process.terminate()
            self.log_output("\n[STOPPED]")

    def execute_process(self, interpreter_file):
        try:
            self.process = subprocess.Popen(
                [sys.executable, interpreter_file, "temp_run.sp"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, bufsize=1, encoding='utf-8'
            )
            for line in iter(self.process.stdout.readline, ''):
                self.console.after(0, self.log_output, line.strip())
            
            err = self.process.stderr.read()
            if err: self.console.after(0, self.log_output, f"\n[ERROR]\n{err}")
            
            self.process.wait()
        finally:
            self.process = None
            self.root.after(0, lambda: self.run_btn.config(state="normal"))
            self.root.after(0, lambda: self.stop_btn.config(state="disabled"))
            self.root.after(0, lambda: self.status_label.config(text="Ready", fg="white"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SapphireIDE(root)
    root.mainloop()