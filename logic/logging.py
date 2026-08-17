from datetime import datetime
import os
import subprocess
import sys


class NullLogger:
    def log_message(self, message, tag="info"):
        return None


class Logging:
    def __init__(self, log_text_widget, status_var=None):
        self.log_text = log_text_widget
        self.status_var = status_var

    def log_message(self, message, tag="info"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"

        self._append_to_widget(formatted_message, tag)

        if self.status_var is not None:
            self.status_var.set(message)

        self._append_to_file(formatted_message)

    def _append_to_widget(self, formatted_message, tag):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", formatted_message, tag)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _append_to_file(self, formatted_message):
        log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}.txt"
        try:
            directory = os.path.dirname(log_file)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(log_file, "a", encoding="utf-8") as file:
                file.write(formatted_message)
        except Exception:
            pass

    def save_to_file(self, file_path):
        content = self.log_text.get("1.0", "end")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    def append_test_message(self, message="Test log entry from button"):
        self.log_message(message, "info")
        self.log_message(message, "success")
        self.log_message(message, "error")
        self.log_message(message, "warning")

    def open_log_file(self):
        log_file = f"log-{datetime.now().strftime('%d/%m/%Y')}.txt"
        if os.path.exists(log_file):
            if os.name == "nt":
                os.startfile(log_file)
            elif os.name == "posix":
                subprocess.call(("open" if sys.platform == "darwin" else "xdg-open", log_file))
        else:
            self.log_message("Log file does not exist.", "error")
