import tkinter as tk


class CustomInputDialog(tk.Toplevel):
    def __init__(self, parent, title, message, OneLetter=False):
        super().__init__(parent)
        self.title(title)
        self.result = None  # default value
        self.label = tk.Label(self, text=message)
        self.label.pack(padx=10, pady=10)

        validate_command = (
            (self.register(self.validate_input), "%P") if OneLetter else None
        )
        self.entry = tk.Entry(self, validate="key", validatecommand=validate_command)
        self.entry.pack(padx=10, pady=10)
        self.entry.bind("<Return>", lambda event=None: self.on_ok())
        self.entry.focus_set()

        self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.cancel_button = tk.Button(self, text="Cancel", command=self.on_cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=10, pady=10)

        x_pos = parent.winfo_x() + 520
        y_pos = parent.winfo_y() + 10
        self.geometry(f"+{x_pos}+{y_pos}")

    def validate_input(self, new_value):
        """Validate the input to allow only one character"""
        return len(new_value) <= 1

    def on_ok(self):
        """on clicking OK button"""
        self.result = self.entry.get()
        self.destroy()

    def on_cancel(self):
        """on clicking cancel button"""
        self.result = None
        self.destroy()
