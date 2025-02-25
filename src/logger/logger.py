import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class Logger:
    _instance: "Logger | None" = None
    _info_box: ScrolledText

    def __new__(cls, infobox: ScrolledText):
        if cls._instance is None:
            if not isinstance(infobox, ScrolledText):  # Ensure valid infobox
                raise TypeError("infobox must be an instance of ScrolledText")
            cls._instance = super().__new__(cls)
            cls._instance._info_box = infobox  # Now recognized
        return cls._instance

    def log_message(self, message: str) -> None:
        if self._info_box is None:
            return
        self._info_box.insert(tk.END, message + "\n")
        self._info_box.yview(tk.END)

    @classmethod
    def get_instance(cls) -> "Logger":
        """Returns the existing Logger instance."""
        if cls._instance is None:
            raise RuntimeError("Logger has not been initialized yet.")
        return cls._instance
