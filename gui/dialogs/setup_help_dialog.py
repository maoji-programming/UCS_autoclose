def show_setup_help(self):
        """Show setup help dialog"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Setup Help")
        help_window.geometry("600x400")
        help_window.transient(self.root)
        help_window.grab_set()
        
        help_text = """
🚀 Welcome to ASUS SIP Auto Downloader!

To get started, please configure the following:

1. 👤 CREDENTIALS:
   - Username: Your ASUS login username
   - Password: Your ASUS login password

2. 🌐 CHROME SETTINGS:
   - Chrome Path: Path to chrome.exe (usually in Program Files)
   - Driver Path: Path to chromedriver.exe (download from Chrome website)

3. 📋 SERIAL NUMBERS:
   - Create a SN.txt file with one serial number per line
   - Or use the "Load File" button to load from any text file
   - Or add individual serial numbers using "Add SN"

4. ⚙️ RECOMMENDED CHROME SETUP:
   - Download ChromeDriver from: https://chromedriver.chromium.org/
   - Make sure ChromeDriver version matches your Chrome version
   - Place chromedriver.exe in a folder (e.g., ./chromedriver/)

Click "Save Config" to save your settings for next time!
        """
        
        text_widget = scrolledtext.ScrolledText(help_window, wrap="word", padx=10, pady=10)
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")
        
        ttk.Button(help_window, text="Close", command=help_window.destroy).pack(pady=10)