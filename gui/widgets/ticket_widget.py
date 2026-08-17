import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class TicketWidget(ttk.Frame):
    def __init__(self, parent, config, automation, logger=None, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill="both", expand=True)
        self.config = config
        self.automation = automation
        self.logger = logger

        self._create()

    
    def load_batch_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Batch File",
            filetypes=[("Text Files", "*.txt")]
        )

        if not file_path:
            return  # User cancelled

        self.batch_records = []  # Clear previous records

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):  # Skip empty lines or comments
                        continue

                    parts = line.replace(" ","").split(";")

                    if len(parts) != 3:
                        messagebox.showerror("Format Error", f"Line {line_number} is invalid:\n{line}")
                        continue

                    org_sn, new_sn, pass_type = map(str.strip, parts)

                    if pass_type not in ["ECN", "Normal"]:
                        messagebox.showerror("Value Error", f"Line {line_number} has invalid pass type:\n{line}")
                        continue

                        
                    self.batch_records.append((org_sn, new_sn, pass_type))
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            for record in self.batch_records:
                self.tree.insert("", "end", values=record)
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to load file:\n{str(e)}")

    def close_single_ticket(self):
        #Clear previous records
        self.batch_records = []
        self.batch_records.append((self.org_sn_var.get().strip(), self.new_sn_var.get().strip(), self.pass_type_var.get().strip()))
        self.start_process()
        pass


    def close_multiple_ticket(self):
        #clear single record
        self.org_sn_var.set("")
        self.new_sn_var.set("")
        self.pass_type_var.set("ECN")
        if not hasattr(self, 'batch_records') or not self.batch_records:
            messagebox.showwarning("No Data", "No batch records to process. Please load a batch file.")
            return
        self.start_process()
        pass


    def start_process(self):
        # Example logic (can call Automation here)
        print("Starting...")
        print("Single Tab - Org SN:", self.org_sn_var.get())
        print("Single Tab - New SN:", self.new_sn_var.get())
        print("Pass Type:", self.pass_type_var.get())
        self.automation.close_ticket(self.batch_records)

    def _create(self):
        ticket_frame = ttk.LabelFrame(self.parent, text="Step 2. Close Ticket")
        ticket_frame.pack(fill="both", expand=True, pady=(0, 10))
        tk_header_frame = ttk.Frame(ticket_frame)
        tk_header_frame.pack(fill="both", pady=(0, 10))

        notebook = ttk.Notebook(ticket_frame)
        notebook.pack(fill="both", expand=True)

        self.single_tab = ttk.Frame(notebook)
        self.multiple_tab = ttk.Frame(notebook)

        notebook.add(self.single_tab, text="Single")
        notebook.add(self.multiple_tab, text="Multiple")

        self._create_single_tab()
        self._create_multiple_tab()
    
    def __force_uppercase(self,*args):
        self.org_sn_var.set(self.org_sn_var.get().upper())

    def _create_single_tab(self):
        frame = ttk.LabelFrame(self.single_tab, text="Close Single Ticket", padding=10)
        frame.pack(fill="x", padx=10, pady=10)


        # New SN
        ttk.Label(frame, text="New SN:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.new_sn_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.new_sn_var).grid(row=0, column=1, padx=5, pady=5)
        # Org SN
        ttk.Label(frame, text="Org SN (minimum last 5 digit):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.org_sn_var = tk.StringVar()
        self.org_sn_var.trace_add("write", self.__force_uppercase)
        ttk.Entry(frame, textvariable=self.org_sn_var).grid(row=1, column=1, padx=5, pady=5)

        # Radio Button
        self.pass_type_var = tk.StringVar(value="ECN")
        ttk.Label(frame, text="Pass Type:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        radio_frame = ttk.Frame(frame)
        radio_frame.grid(row=2, column=1, padx=5, pady=5)

        ttk.Radiobutton(radio_frame, text="ECN Pass", variable=self.pass_type_var, value="ECN").pack(side="left", padx=5)
        ttk.Radiobutton(radio_frame, text="Normal Pass", variable=self.pass_type_var, value="Normal").pack(side="left", padx=5)
        # Load file button
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=1, pady=(10, 0))
        ttk.Button(button_frame, text="Start Automation", command=self.close_single_ticket).pack(side="left", padx=5)

    def _create_multiple_tab(self):
        frame = ttk.LabelFrame(self.multiple_tab, text="Close Multiple Tickets", padding=10)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        
        table_frame = ttk.Frame(frame)
        table_frame.grid(row=1, column=0, columnspan=1, pady=(10, 0))

        #instruction label
        instruction_text = (
            "In your batch file, each line must follow the format: <Org SN>;<New SN>;<Pass Type>\n"
            "Pass Type must be either: ECN or Normal\n\n"
            "Example:\n"
            "12345 ; S12345657890123 ; Normal"
        )
        format_label_frame = ttk.Frame(frame)
        format_label_frame.grid(row=0, column=0, columnspan=1, pady=(5, 0), sticky="w")
        format_label = ttk.Label(format_label_frame, text=instruction_text, foreground="gray")
        format_label.pack(padx=10, pady=(5, 15), anchor="w")
        # Table (Treeview)
        self.tree = ttk.Treeview(table_frame, columns=("org_sn", "new_sn", "pass_type"), show="headings", height=7)
        self.tree.heading("org_sn", text="Org SN")
        self.tree.heading("new_sn", text="New SN")
        self.tree.heading("pass_type", text="Pass Type")

        self.tree.column("org_sn", width=150, stretch=False, anchor="w")
        self.tree.column("new_sn", width=150, stretch=False, anchor="w")
        self.tree.column("pass_type", width=100, stretch=False, anchor="w")

        # Load file and Start button
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=1, pady=(5, 0))
        self.tree.pack(fill="both", expand=True, pady=10)
        ttk.Button(button_frame, text="Load Batch File", command=self.load_batch_file).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="Start Automation", command=self.close_multiple_ticket).pack(side="left", padx=(0, 10))

