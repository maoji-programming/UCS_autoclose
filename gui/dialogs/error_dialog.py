import tkinter.messagebox as msgbox

def show_confirmation_dialog(parent):
    return msgbox.askyesno("Confirm", "Are you sure you want to close the incident?")
