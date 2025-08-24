import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext

from gui.widgets.login_widget import LoginWidget
import config as AppConfig
from logic.automation import Automation
from gui.widgets.ticket_widget import TicketWidget

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
        self.geometry("600x800")
        self.minsize(600, 800)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.config = AppConfig.get_instance()
        self.automation = Automation(self.config)

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
        LoginWidget(self, self.config)
        TicketWidget(self, self.config)
        
        

        pass