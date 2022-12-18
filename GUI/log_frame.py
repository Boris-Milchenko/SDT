from tkinter import ttk
import tkinter as tk

class Log(ttk.Frame):
    def __init__(self, container, text=None):
        super().__init__(container)

        self.label = ttk.Label(self, text = text)
        self.label.pack(fill='y', expand=True)

        self.pack(fill='y', expand=True)

    def Out(self, text):
        self.label['text'] = text
