import datetime
import os
import subprocess

class Logging:

    def __init__(self, log_text_widget, status_var):
        self.log_text = log_text_widget
        self.status_var = status_var

    def log_message(self, message, tag="normal"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert("end", formatted_message, tag)
        self.log_text.see("end")
        self.status_var.set(message)
        
        # Auto-save logs to file
        try:
            with open(f"log-{datetime.now().strftime("%d/%m/%Y")}.txt", "a", encoding="utf-8") as f:
                f.write(formatted_message)
        except:
            pass  # Ignore file write errors
    def open_log_file(self):
        log_file = f"log-{datetime.now().strftime("%d/%m/%Y")}.txt"
        if os.path.exists(log_file):
            if os.name == 'nt':  # Windows
                os.startfile(log_file)
            elif os.name == 'posix':  # macOS or Linux
                subprocess.call(('open' if sys.platform == 'darwin' else 'xdg-open', log_file))
        else:
            self.log_message("Log file does not exist.", "error")
    