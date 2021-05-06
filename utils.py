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
        summary = []
        for f in self.menu.children.values():
            if isinstance(f, tk.Frame):
                if f.sum > 0:
                    summ = {}
                    summ['product'] = str(f.product)
                    summ['price'] = str(f.price)
                    summ['quantity'] = 'x' + str(f.quantity)
                    summ['sum'] = str(f.sum)
                    summary.append(summ)
        artikel = tk.Label(self, text='ARTIKAL')
        artikel.grid()
        cena = tk.Label(self, text='CENA')
        cena.grid(row=0, column=1, padx=5, pady=5)
        kolicina = tk.Label(self, text='KOL.')
        kolicina.grid(row=0, column=2) 
        ukupno = tk.Label(self, text='UKUPNO')
        ukupno.grid(row=0, column=3)

        for i, s in enumerate(summary, 1):
            print(i)
            for idx, value in enumerate(s.values()):
                val_lab = tk.Label(self, text=value)
                if i == 0:
                   val_lab['anchor'] = 'w'
                val_lab.grid(row=i, column=idx)

        sony_price = self.sony.price
        start = len(summary)
        for i in sony_price:
            sony_lab = tk.Label(self, text='SONY')
            sony_lab.grid(row=start+1, column=0)
            sony_price = tk.Label(self, text=i)
            sony_price.grid(row=start+1, column=3)
            start += 1


        total = sum([int(x['sum']) for x in summary]) + sum(self.menu.sony.price)
        total_lab = tk.Label(self, text=total, font=("Arial Bold", 15))
        total_lab.grid(column=3)

        pay_btn = tk.Button(self, text='NAPLATI', command=self.pay, background='green', foreground='white')
        pay_btn.grid(columnspan=4, sticky='NWES')
        self.bind("<Escape>", lambda event: self.cancel_pressed())
        self.resizable(False, False)

    def pay(self):
        self.sony.pay = True
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def buttonbox(self):
      pass # leave this way so it overwrites pack manager used in base class
