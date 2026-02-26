import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext

from logic.automation import Automation

class LogWidget(ttk.Frame):
    def __init__(self, parent, config, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill="both", expand=True)
        self.config = config

        self._create()

    def _create(self):
        """Create log section"""
        log_frame = ttk.LabelFrame(self.parent, text="Activity Logs", padding="10")
        log_frame.pack(fill="both", expand=True)
        
        # Log text with scrollbar
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap="word", font=('Consolas', 9))
        self.log_text.pack(fill="both", expand=True)
        
        # Configure text tags for colored output
        self.log_text.tag_configure("success", foreground="green")
        self.log_text.tag_configure("error", foreground="red")
        self.log_text.tag_configure("warning", foreground="orange")
        self.log_text.tag_configure("info", foreground="blue")