

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from logic.automation import Automation

class LoginWidget(ttk.Frame):
    def __init__(self, parent, config, automation, logger=None, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill="both", expand=True)
        self.config = config
        self.automation = automation
        self.logger = logger

        self._create()
        self.load_setting()
        

    def browse_chrome_path(self):
        path = filedialog.askopenfilename(
            title="Select Chrome Executable",
            filetypes=[("Executable Files", "*.exe")]
        )
        if path:
            self.chrome_path_var.set(path)

    def browse_driver_path(self):
        path = filedialog.askopenfilename(
            title="Select Chrome Driver",
            filetypes=[("Executable Files", "*.exe")]
        )
        if path:
            self.driver_path_var.set(path)

    def load_setting(self):
        
        self.username_var.set(self.config.get('username', ''))
        self.password_var.set(self.config.get('password', ''))
        self.chrome_path_var.set(self.config.get('chrome_path', ''))
        self.driver_path_var.set(self.config.get('driver_path', ''))

    def clean(self):
        """Reset configuration to defaults"""
        if messagebox.askyesno("Clean Configuration", "Are you sure you want to clean all configuration?"):
            self.username_var.set("")
            self.password_var.set("")
            self.chrome_path_var.set("")
            self.driver_path_var.set("")
            if self.logger:
                self.logger.log_message("Configuration cleaned", "info")
    
    def login(self):
        """Perform login action"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        chrome_path = self.chrome_path_var.get().strip()
        driver_path = self.driver_path_var.get().strip()

        if not username or not password or not chrome_path or not driver_path:
            messagebox.showerror("Input Error", "All fields are required.")
            if self.logger:
                self.logger.log_message("Login attempt failed: missing fields", "error")
            return
        
        if self.logger:
            self.logger.log_message("Login button clicked", "info")

        success, message = self.automation.login(username, password, chrome_path, driver_path)
        if success:
            if self.logger:
                self.logger.log_message("Login started successfully", "success")
            messagebox.showinfo("Login Required", "Please enter the verification code and OTP on the browser and complete the login process.")
        else:
            if self.logger:
                self.logger.log_message(f"Login failed: {message}", "error")
            messagebox.showerror("Login Failed", "Login failed. Please check your credentials and paths.")

    def _create(self):
        """Create configuration section"""
        config_frame = ttk.LabelFrame(self.parent, text="Step 1. UCS Login", padding="10")
        config_frame.pack(fill="x")
        
        # Create grid layout
        config_frame.columnconfigure(1, weight=1)
        config_frame.columnconfigure(3, weight=1)
        
        # Username and Password
        ttk.Label(config_frame, text="Username:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(config_frame, textvariable=self.username_var, width=25)
        username_entry.grid(row=0, column=1, sticky="ew", padx=(0, 20), pady=5)
        
        ttk.Label(config_frame, text="Password:", font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky="w", padx=(0, 10), pady=5)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(config_frame, textvariable=self.password_var, show="*", width=25)
        password_entry.grid(row=0, column=3, sticky="ew", pady=5)
        
        # Chrome Path
        ttk.Label(config_frame, text="Chrome Path:", font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        self.chrome_path_var = tk.StringVar()
        chrome_entry = ttk.Entry(config_frame, textvariable=self.chrome_path_var)
        chrome_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(0, 10), pady=5)
        ttk.Button(config_frame, text="Browse", command=self.browse_chrome_path).grid(row=1, column=3, sticky="w", pady=5)
        
        # Driver Path
        ttk.Label(config_frame, text="Driver Path:", font=('Arial', 9, 'bold')).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)
        self.driver_path_var = tk.StringVar()
        driver_entry = ttk.Entry(config_frame, textvariable=self.driver_path_var)
        driver_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=(0, 10), pady=5)
        ttk.Button(config_frame, text="Browse", command=self.browse_driver_path).grid(row=2, column=3, sticky="w", pady=5)
        
        # Config buttons
        button_frame = ttk.Frame(config_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=(15, 0))
        
        ttk.Button(button_frame, text="Load Setting", command=self.load_setting).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="Clean", command=self.clean).pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame, text="Login", command=self.login).pack(side="left", padx=(0, 10))
