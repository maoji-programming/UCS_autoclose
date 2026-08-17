import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext

from logic.logging import Logging


class LogWidget(ttk.Frame):
    def __init__(self, parent, config, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill="both", expand=True)
        self.config = config

        self._create()

    def _create(self):
        """Create log section"""
        log_frame = ttk.LabelFrame(self, text="Activity Logs", padding="10")
        log_frame.pack(fill="both", expand=True)

        button_frame = ttk.Frame(log_frame)
        button_frame.pack(fill="x", pady=(0, 8))

        ttk.Button(button_frame, text="Write a line", command=self.write_test_line).pack(side="left", padx=(0, 5))
        ttk.Button(button_frame, text="Save Log File", command=self.save_log_file).pack(side="left")

        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap="word", font=('Consolas', 9))
        self.log_text.pack(fill="both", expand=True)
        self.log_text.configure(state="disabled")

        self.log_text.tag_configure("success", foreground="green")
        self.log_text.tag_configure("error", foreground="red")
        self.log_text.tag_configure("warning", foreground="orange")
        self.log_text.tag_configure("info", foreground="blue")

        self.status_var = tk.StringVar(value="")
        self.logger = Logging(self.log_text, self.status_var)

    def write_test_line(self):
        self.logger.append_test_message()

    def save_log_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Log File",
            defaultextension=".log",
            filetypes=[("Log Files", "*.log"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if not file_path:
            return

        try:
            self.logger.save_to_file(file_path)
            messagebox.showinfo("Save Log", f"Log saved to:\n{file_path}")
        except Exception as exc:
            messagebox.showerror("Save Error", f"Could not save log file:\n{exc}")