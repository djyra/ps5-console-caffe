import tkinter as tk

class TimeDialog(tk.simpledialog.Dialog):
    def __init__(self, sony, title):
        self.sony = sony
        super().__init__(sony, title)

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
        self.sony.added_time += 3600
        self.sony.price.append(300)
        self.destroy()

    def two_pressed(self):
        self.sony.seconds_left += 7200
        self.sony.added_time += 7200
        self.sony.price.append(600)
        self.destroy()

    def three_pressed(self):
        self.sony.seconds_left += 10800
        self.sony.added_time += 10800
        self.sony.price.append(800)
        self.destroy()


    def cancel_pressed(self):
        self.destroy()


class ReceiptDialog(tk.simpledialog.Dialog): 
    def __init__(self, title, menu):
        self.menu = menu
        self.sony = menu.sony
        super().__init__(self.sony, title)

    def body(self, frame):
        result = self.menu.show_summary()
        resultt = tk.Label(frame, text=result)
        resultt.grid()
        return frame 

    def pay(self):
        self.sony.pay = True
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def buttonbox(self):
        self.pay_btn = tk.Button(self, text='NAPLATI', command=self.pay)
        self.pay_btn.pack(fill='both')
        self.bind("<Escape>", lambda event: self.cancel_pressed())
