import tkinter as tk
import tkinter.simpledialog

class TimeDialog(tkinter.simpledialog.Dialog):
    def __init__(self, sony, title):
        self.sony = sony
        super().__init__(sony, title)

    def body(self, sony):
        inner_frame = tk.Frame(self)
        inner_frame.pack()
        self.pm_label = tk.Label(inner_frame,
                                  text='A.M. Prices',
                                  anchor='e',
                                  font="-family {Ubuntu Condensed} -size 14 -weight bold")
        self.pm_label.grid(column=0, row=0, columnspan=2,  sticky='W')

        self.one_button_am = tk.Button(inner_frame,
                                    text='1h \n 6 €',
                                    width=5,
                                    height=3,
                                    fg='black',
                                    font="-family {Ubuntu Condensed} -size 16 -weight bold",
                                    cursor='hand2',
                                    command=self.one_pressed_am)
        self.one_button_am.grid(column=0, row=1, sticky='NWES')


        self.two_button_am = tk.Button(inner_frame,
                                    text='2h \n 10 €',
                                    width=5,
                                    height=3,
                                    fg='black',
                                    font="-family {Ubuntu Condensed} -size 16 -weight bold",
                                    cursor='hand2',
                                    bg='blue',
                                    command=self.two_pressed_am)
        self.two_button_am.grid(column=1, row=1, sticky='NWES')

        self.three_button_am = tk.Button(inner_frame,
                                      text='3h \n 15 €',
                                      width=5,
                                      height=3,
                                      fg='black',
                                      font="-family {Ubuntu Condensed} -size 16 -weight bold",
                                      cursor='hand2',
                                      command=self.three_pressed_am)
        self.three_button_am.grid(column=2, row=1, sticky='NWES')

        # PRICES PM
        self.pm_label = tk.Label(inner_frame,
                                  text='P.M. Prices',
                                  anchor='e',
                                  font="-family {Ubuntu Condensed} -size 14 -weight bold")
        self.pm_label.grid(column=0, row=2, columnspan=2,  sticky='W')


        self.one_button = tk.Button(inner_frame,
                                    text='1h \n 8 €',
                                    width=5,
                                    height=3,
                                    fg='black',
                                    font="-family {Ubuntu Condensed} -size 16 -weight bold",
                                    cursor='hand2',
                                    command=self.one_pressed)
        self.one_button.grid(column=0, row=3, sticky='NWES')

        self.two_button = tk.Button(inner_frame,
                                    text='2h \n 15 €',
                                    width=5,
                                    height=3,
                                    fg='black',
                                    font="-family {Ubuntu Condensed} -size 16 -weight bold",
                                    cursor='hand2',
                                    command=self.two_pressed)
        self.two_button.grid(column=1, row=3, sticky='NWES')

        self.three_button = tk.Button(inner_frame,
                                      text='3h \n 22€',
                                      width=5,
                                      height=3,
                                      fg='black',
                                      font="-family {Ubuntu Condensed} -size 16 -weight bold",
                                      cursor='hand2',
                                      command=self.three_pressed)

        self.three_button.grid(column=2, row=3, sticky='NWES')
        self.resizable(False, False)

    def buttonbox(self):
        # exit on escape btn
        self.bind("<Escape>", lambda event: self.cancel_pressed())

    # have to do it manually like this instead of making a function
    # and passing arguments through property command of tk.Button 
    # i was messing around with it a bit wit no luck and its working like this so its ok
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

