import tkinter as tk
from tkinter import simpledialog

class TimeDialog(tk.simpledialog.Dialog):
    def __init__(self, master, sony, title):
        self.sony = sony
        super().__init__(master, title)

    def buttonbox(self):
        self.one_button = tk.Button(self, text='1', width=5, command=self.one_pressed)
        self.one_button.pack(side="left")

        self.two_button = tk.Button(self, text='2', width=5, command=self.two_pressed)
        self.two_button.pack(side='left')

        self.three_button = tk.Button(self, text='3', width=5, command=self.three_pressed)
        self.three_button.pack(side='left')

        self.bind("<Escape>", lambda event: self.cancel_pressed())


    def one_pressed(self):
        self.sony.seconds_left += 3600
        self.sony.price += 350
        self.destroy()

    def two_pressed(self):
        self.sony.seconds_left += 7200
        self.sony.price += 600
        self.destroy()

    def three_pressed(self):
        self.sony.seconds_left += 10800
        self.sony.price += 800
        self.destroy()


    def cancel_pressed(self):
        self.destroy()

