import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

def show_manual_dialog():
    result = messagebox.askokcancel(
        "Manual Action Required",
        "Please complete the following steps in the browser:\n\n"
        "1. Complete CAPTCHA if present\n"
        "2. Click Login button\n"
        "3. Enter OTP when prompted\n"
        "4. Wait for dashboard to load\n\n"
        "Click OK when you've completed all steps and reached the dashboard.\n"
        "Click Cancel to abort the process."
    )
    return result