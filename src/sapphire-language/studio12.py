# ----------------------------------------------------------------------
# Sapphire Studio v1.2: Stable Basic Engine (more Pygame shapes and abort() command)
# Made by: GitHub@CodeyWaffle & Gemini AI
# ----------------------------------------------------------------------
import tkinter as tk
from tkinter import scrolledtext, PanedWindow, messagebox, filedialog
import subprocess
import sys
import os
import threading
import shutil
import sapphire-language.engine12 as engine


class SapphireIDE:
    def __init__(self, root):
        self.root = root
        BASE_PATH = os.path.dirname(__file__)
        ICON_PATH = os.path.join(BASE_PATH, "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(ICON_PATH)
            except:
                pass
        
        self.root.title(" Sapphire Studio v1.2")
        self.root.geometry("1100x700")
        
        # --- PHASE 2: DEFINE PATHS ---
        # Look one level up from /config to find /SapphireProjects
        self.workspace_path = os.path.abspath(os.path.join(os.getcwd(), "..", "SapphireProjects"))
        self.current_file = None
        self.root.geometry("1100x700")
        self.process = None
        self.current_file = "Untitled.sp"
        
        # --- 1. Top Toolbar ---
        self.toolbar = tk.Frame(root, bg="#2d2d2d", height=40)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # VERSION SELECTOR
        
        self.ver_label = tk.Label(self.toolbar, text="v1.7.0", font=("Segoe UI", 10, "bold"),fg="#ffffff", bg="#333333")
        self.ver_label.pack(side=tk.LEFT, padx=2)

        # Buttons
        self.new_btn = tk.Button(self.toolbar, text="+ New", command=self.new_file, bg="#003047", fg="white", font=("Segoe UI", 9, "bold"), padx=10, pady=2, bd=0, cursor="hand2")
        self.new_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.run_btn = tk.Button(self.toolbar, text="▶ Run", command=self.run_code, bg="#00456D", fg="white", font=("Segoe UI", 9, "bold"), padx=10, pady=2, bd=0, cursor="hand2")
        self.run_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_btn = tk.Button(self.toolbar, text="■ Stop", command=self.stop_code, bg="#006494", fg="white", font=("Segoe UI", 9, "bold"), padx=10, pady=2, bd=0, cursor="hand2", state="disabled")
        self.stop_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_btn = tk.Button(self.toolbar, text="💾 Save", command=self.save_file, bg="#0582ca", fg="white", font=("Segoe UI", 9, "bold"), padx=10, pady=2, bd=0, cursor="hand2")
        self.save_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.load_btn = tk.Button(self.toolbar, text="📂 Load", command=self.load_file, bg="#00a6fb", fg="white", font=("Segoe UI", 9, "bold"), padx=10, pady=2, bd=0, cursor="hand2")
        self.load_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.status_label = tk.Label(self.toolbar, text="Ready", bg="#2d2d2d", fg="white", font=("Segoe UI", 9, "bold"))
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # --- 2. Layout ---
        self.panes = PanedWindow(root, orient=tk.HORIZONTAL, bg="#1e1e1e", sashwidth=6, sashrelief=tk.RAISED)
        self.panes.pack(fill=tk.BOTH, expand=True)

        self.editor = scrolledtext.ScrolledText(self.panes, font=("Consolas", 12), bg="#252526", fg="#d4d4d4", insertbackground="white", undo=True)
        self.panes.add(self.editor, minsize=300)

        self.console = scrolledtext.ScrolledText(self.panes, state='disabled', font=("Segoe UI", 11), bg="#000000", fg="#00ff00")
        self.panes.add(self.console, minsize=200)

        # Load Welcome Code on Start
        self.load_welcome_code()
    def log_output(self, text):
        self.console.config(state='normal')
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.config(state='disabled')
    def save_file(self):
        if not self.current_file or self.current_file == "Untitled.sp":
            file_path = filedialog.asksaveasfilename(
                initialdir=self.workspace_path,
                defaultextension=".sp",
                filetypes=[("Sapphire Script", "*.sp"), ("All Files", "*.*")]
            )
            if not file_path: return # user denial
            self.current_file = file_path

        code = self.editor.get("1.0", "end-1c")

        try:
            # 1. Save to current file
            with open(self.current_file, "w", encoding='utf-8') as f:
                f.write(code)

            # 2. Logic check
            project_dir = os.path.abspath(self.workspace_path)
            save_dir = os.path.abspath(os.path.dirname(self.current_file))

            if project_dir != save_dir:
                filename = os.path.basename(self.current_file)
                backup_path = os.path.join(project_dir, filename)
                with open(backup_path, "w", encoding='utf-8') as f:
                    f.write(code)
                print(f"💎 Sapphire: Double-saved to {backup_path}")

            # Update window title and status
            project_name = os.path.basename(self.current_file)
            self.root.title(f"Editing: {project_name} - Sapphire Studio")
            self.status_label.config(text=f"Project Saved: {project_name}", fg="#3498db")

        except Exception as e:
            messagebox.showerror("Save Error", f"Save failed: {str(e)}")

        
        if file_path:
            self.current_file = file_path
            with open(self.current_file, "w", encoding='utf-8') as f:
                f.write(self.editor.get("1.0", tk.END))
            
            project_name = os.path.basename(file_path)
            self.root.title(f"Editing: {project_name} - Sapphire Studio")
            self.status_label.config(text=f"Project Saved: {project_name}", fg="#3498db")
    
    def detect_version(self):
        files = [f for f in os.listdir('.') if f.startswith('Sapphire') and f.endswith('.py') and f != 'SapphireStudio12.py']
        if not files: return "17" # Default to latest version
        latest = sorted(files, reverse=True)[0]
        return latest.replace('Sapphire', '').replace('.py', '')
    
    def load_file(self):
        # Allow loading from anywhere on the computer
        file_path = filedialog.askopenfilename(
            filetypes=[("Sapphire Script", "*.sp"), ("All Files", "*.*")]
        )
    
        if file_path:
            with open(file_path, "r", encoding='utf-8') as f:
                content = f.read()
                self.editor.delete("1.0", "end")
                self.editor.insert("1.0", content)
            print(f"💎 Sapphire: Loaded {file_path}")
    def load_welcome_code(self):
        welcome = """// 💎 Welcome to Sapphire v1.7
setup {
    //this is a comment.
    //this is a setup area that runs once at the start
    var str(greeting){"Hello, Sapphire Developer!"}
    println(var str greeting)
}

main {
    // this is a main loop that runs continuously
    println("System is active and running.")
    abort() // stops the program after one loop
}
"""
        self.editor.insert("1.0", welcome)

    def new_file(self):
        if messagebox.askyesno("New File", "Discard current code and start fresh?"):
            self.editor.delete("1.0", tk.END)
            template = "setup {\n    \n}\n\nmain {\n    \n}"
            self.editor.insert("1.0", template)
            self.status_label.config(text="New Template Loaded", fg="#9b59b6")


    def run_code(self):
        
        interpreter_file = os.path.abspath(engine.__file__)

        if not os.path.exists(interpreter_file):
            messagebox.showerror("Error", "Sapphire Engine not found in package!")
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
    def stop_game(self):
    # Only try to kill the process if it actually exists and is running
        if hasattr(self, 'game_process'):
            if self.game_process.poll() is None: 
                self.game_process.terminate()
                print("Stopped.")
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
