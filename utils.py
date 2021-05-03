import tkinter as tk

class TimeDialog(tk.simpledialog.Dialog):
    def __init__(self, sony, title):
        self.sony = sony
        super().__init__(sony, title)

    def body(self, sony):

        #PRICES AM
        self.pm_label = tk.Label(self,
                                 text='PREPODNE',
                                 anchor='e',
                                 font="-family {Ubuntu Condensed} -size 14 -weight bold")
        self.pm_label.grid(column=0, row=0, columnspan=2,  sticky='W')

        self.one_button_am = tk.Button(self, 
                                    text='1h \n 300 RSD', 
                                    width=5,
                                    height=3,
                                    fg='white',
                                    bg='blue',
                                    font="-family {Ubuntu Condensed} -size 10 -weight bold",
                                    cursor='hand2',
                                    command=self.one_pressed_am)
        self.one_button_am.grid(column=0, row=1, sticky='NWES')


        self.two_button_am = tk.Button(self,
                                    text='2h \n 500 RSD',
                                    width=5,
                                    height=3,
                                    fg='white',
                                    font="-family {Ubuntu Condensed} -size 10 -weight bold",
                                    cursor='hand2',
                                    bg='blue',
                                    command=self.two_pressed_am)
        self.two_button_am.grid(column=1, row=1, sticky='NWES')

        self.three_button_am = tk.Button(self,
                                      text='3h \n 600 RSD', 
                                      width=5,
                                      height=3,
                                      fg='white',
                                      font="-family {Ubuntu Condensed} -size 10 -weight bold",
                                      cursor='hand2',
                                      bg='blue',
                                      command=self.three_pressed_am)
        self.three_button_am.grid(column=2, row=1, sticky='NWES')
 
        # PRICES PM
        self.pm_label = tk.Label(self,
                                 text='POPODNE',
                                 anchor='e',
                                 font="-family {Ubuntu Condensed} -size 14 -weight bold")
        self.pm_label.grid(column=0, row=2, columnspan=2,  sticky='W')


        self.one_button = tk.Button(self, 
                                    text='1h \n 350 RSD', 
                                    width=5,
                                    height=3,
                                    fg='white',
                                    bg='green',
                                    font="-family {Ubuntu Condensed} -size 10 -weight bold",
                                    cursor='hand2',
                                    command=self.one_pressed)
        self.one_button.grid(column=0, row=3, sticky='NWES')

        self.two_button = tk.Button(self,
                                    text='2h \n 600 RSD',
                                    width=5,
                                    height=3,
                                    fg='white',
                                    font="-family {Ubuntu Condensed} -size 10 -weight bold",
                                    cursor='hand2',
                                    bg='green',
                                    command=self.two_pressed)
        self.two_button.grid(column=1, row=3, sticky='NWES')

        self.three_button = tk.Button(self,
                                      text='3h \n 800 RSD', 
                                      width=5,
                                      height=3,
                                      fg='white',
                                      font="-family {Ubuntu Condensed} -size 10 -weight bold",
                                      cursor='hand2',
                                      bg='green',
                                      command=self.three_pressed)
        self.three_button.grid(column=2, row=3, sticky='NWES')
        self.resizable(False, False) 

    def buttonbox(self):
        self.bind("<Escape>", lambda event: self.cancel_pressed())

    def one_pressed(self):
        self.sony.seconds_left += 3600
        self.sony.added_time += 3600
        self.sony.price.append(350)
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

    def one_pressed_am(self):
        self.sony.seconds_left += 3600
        self.sony.added_time += 3600
        self.sony.price.append(300)
        self.destroy()

    def two_pressed_am(self):
        self.sony.seconds_left += 7200
        self.sony.added_time += 7200
        self.sony.price.append(500)
        self.destroy()

    def three_pressed_am(self):
        self.sony.seconds_left += 10800
        self.sony.added_time += 10800
        self.sony.price.append(600)
        self.destroy()



    def cancel_pressed(self):
        self.destroy()


class ReceiptDialog(tk.simpledialog.Dialog): 
    def __init__(self, menu, title):
        self.menu = menu
        self.sony = menu.sony
        super().__init__(self.sony, title)

    def body(self, menu):
        result = self.menu.show_summary()
        resultt = tk.Label(self, text=result)
        resultt.grid()
        self.resizable(False, False)

    def pay(self):
        self.sony.pay = True
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def buttonbox(self):
        self.pay_btn = tk.Button(self, text='NAPLATI', command=self.pay)
        self.pay_btn.grid()
        self.bind("<Escape>", lambda event: self.cancel_pressed())
