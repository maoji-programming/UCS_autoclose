import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext


import config as AppConfig
from logic.automation import Automation

from gui.widgets.login_widget import LoginWidget
from gui.widgets.ticket_widget import TicketWidget
from gui.widgets.log_widget import LogWidget

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.stats = {
            'processed': 0,
            'success': 0,
            'failed': 0,
            'waiting': 0
        }
        self.title("RMA Incident Closer")
        self.geometry("600x600")
        self.minsize(800, 600)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.config = AppConfig.get_instance()
        self.driver = None
        self.automation = None

        # Configure style
        self.setup_styles()
        # Create GUI components
        self._setup_widgets()


    def setup_styles(self):    
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Success.TLabel', foreground='green', font=('Arial', 9, 'bold'))
        style.configure('Error.TLabel', foreground='red', font=('Arial', 9, 'bold'))
        style.configure('Warning.TLabel', foreground='orange', font=('Arial', 9, 'bold'))
        style.configure('Info.TLabel', foreground='blue', font=('Arial', 9, 'bold'))

        style.configure("Treeview", font=("Courier", 9))  # Row font
        style.configure("Treeview.Heading", font=("Courier", 9, "bold"))  # Header font

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.destroy()

    def _setup_widgets(self):
        main_frame = ttk.Frame(self, padding="5")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="ASUS UCS Auto Close", style='Title.TLabel')
        title_label.pack(pady=(0, 2))
        """
        Create the main GUI components.
        - config section
        - tab 1(single ticket):
            - ticket info section
            - control buttons
            - progress section(Pending/Success/Error)
        - tab 2(batch process):
            - tickets list section
            - control buttons
            - progress section
        - create log section
        - status bar
        """
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)

        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=4)
        content_frame.rowconfigure(0, weight=1)

        left_frame = ttk.Frame(content_frame, padding=(0, 0, 5, 0))
        left_frame.grid(row=0, column=0, sticky="nsew")

        right_frame = ttk.Frame(content_frame, padding=(5, 0, 0, 0))
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        log_widget = LogWidget(right_frame, self.config)
        self.automation = Automation(self.config, logger=log_widget.logger)
        LoginWidget(left_frame, self.config, automation=self.automation, logger=log_widget.logger)
        TicketWidget(left_frame, self.config, automation=self.automation, logger=log_widget.logger)
        
        

        pass