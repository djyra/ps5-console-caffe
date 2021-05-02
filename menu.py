#! /usr/bin/env python

import tkinter as tk
from PIL import Image, ImageTk

from utils import ReceiptDialog

# Menu item class that can be reused for any product
class MenuItem(tk.Frame):
    def __init__(self, master, price, product, image):
        tk.Frame.__init__(self, master, width=675, height=95)
        self.master = master
        self.product = product
        self.image = image
        self.price = price
        self.quantity = 0
        self.sum = 0

        self.configure(relief='groove')
        self.configure(borderwidth="2")
        self.configure(relief="groove")

        self.plus_btn = tk.Button(self)
        self.plus_btn.place(relx=0.844, rely=0.316, height=41, width=41)
        self.plus_btn.configure(cursor="fleur",
                                font="-family {Ubuntu Condensed} -size 20 -weight bold",
                                text='+',
                                command=self.add)

        self.minus_btn = tk.Button(self)
        self.minus_btn.place(relx=0.681, rely=0.316, height=41, width=41)
        self.minus_btn.configure(activebackground="#f9f9f9",
                                font="-family {Ubuntu Condensed} -size 20 -weight bold",
                                text='''-''',
                                command=self.sub)

        self.number = tk.Label(self)
        self.number.place(relx=0.756, rely=0.316, relheight=0.463, relwidth=0.083)
        self.number.configure(background='white',
                                font='-family {Ubuntu Condensed} -size 16 -weight bold',
                                text=f'{self.quantity}')

        self.item_name = tk.Label(self)
        self.item_name.place(relx=0.311, rely=0.211, height=61, width=229)
        self.item_name.configure(anchor='w',
                                cursor='fleur',
                                font='-family {Ubuntu Condensed} -size 16',
                                text=f'{self.product}')

        # TODO pre-format images so it executes faster, remove line below
        self.image = Image.open(self.image).transpose(Image.ROTATE_270) \
                                .resize((200, 50), Image.ANTIALIAS)
        self.ready_image = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self, image = self.ready_image)
        self.image_label.place(relx=0.005, rely=0.20, height=50, width=200)


    def add(self):
        if self.quantity >= 0:
            self.quantity += 1
            self.number['text'] = str(self.quantity)
            self.sum += self.price

    def sub(self):
        if self.quantity >= 1: # can't go negative
            self.quantity -= 1
            self.number['text'] = str(self.quantity)
            self.sum -= self.price


class Menu(tk.Toplevel):
    def __init__(self, master, sony):
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.sony = sony

        # Initialization - needs to be hidden so the logic is easier
        self.withdraw()
        self.title('<>< Snacks and Drinks ><>')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.leave_open)
        self.wm_attributes("-topmost", True)
        self.transient(self.master) # removes min/max
        self.updating = self.after(100, self.update_gui) # has to be done like this so it can be canceled in pay_cash()

    def leave_open(self):
        self.grab_release() # remove grab and withdraw window
        self.withdraw()

    def pay_cash(self):
        dialog = ReceiptDialog(master=self.master, menu=self, title='NAPLATI')
        self.after_cancel(self.updating)
        if self.sony.pay:
            #TODO ADD TO DATABASE

            #restart values in sony.menu
            for f in self.children.values():
                if isinstance(f, tk.Frame):
                    f.sum = 0
                    f.quantity = 0
                    f.number['text'] = 0

    def show_summary(self):
        summary = []
        for f in self.children.values():
            if isinstance(f, tk.Frame):
                if f.sum > 0:
                    summ = {}
                    summ['product'] = str(f.product)
                    summ['quantity'] = str(f.quantity)
                    summ['price'] = str(f.price)
                    summ['sum'] = str(f.sum)
                    summary.append(summ)
        string = ''
        suma = 0
        for s in summary:
            string += s['product']+ ': ' + s['quantity'] + ' x ' + s['price'] + ' = ' + s['sum'] + '\n'
            suma += float(s['sum'])
        money = sum(self.sony.price)
        result = string + str(money) + 'Total: \t\t' + str(suma + money)
        return result

    ## MENU ITEMS
    def fill_gui(self):
        self.item1 = MenuItem(self, image='images/coca.png',
                             product='Koca 0.5',
                             price=3.5)
        self.item1.grid(row=0, column=0, sticky='NWES')

        self.item2 = MenuItem(self, image='images/fanta.png',
                             product='Fanta 0.5',
                             price=3.5)
        self.item2.grid(row=1, column=0, sticky='NS')

        self.item3 = MenuItem(self, image='images/sprite.png',
                             product='Sprite 0.5',
                             price=3.5)
        self.item3.grid(row=2, column=0, sticky='NWES')

        self.item4 = MenuItem(self, image='images/heineken.png',
                           product='Heineken 0.33',
                           price=4)
        self.item4.grid(row=3, column=0, sticky='NWES')

        self.item5 = MenuItem(self, image='images/sandwich.png',
                           product='Sandwich',
                           price=5)
        self.item5.grid(row=4, column=0, sticky='NWES')

        self.item6 = MenuItem(self, image='images/heineken.png',
                           product='Heineken 0.4',
                           price=170)
        self.item6.grid(row=1, column=1, sticky='NS')

        self.racun = tk.Label(self, text='0',
                           font='-family {Ubuntu Condensed} -size 45 -weight bold',
                           foreground='green')
        self.racun.grid(row=5, column=0, sticky='NSEW')

        self.leave_open_btn = tk.Button(self,
                   text='OPEN TAB',
                   background='blue',
                   foreground='white',
                   font='-family {Ubuntu Condensed} -size 20 -weight bold',
                   command=self.leave_open,
                   cursor='hand2')
        self.leave_open_btn.grid(row=6, column=0, sticky='NSEW')

        self.sony_num = tk.Label(self, text=self.sony.sony_num)
        self.sony_num.grid(row=8, column=0, sticky='NWES')

    def update_gui(self):
        total = sum([f.sum for f in self.children.values() if isinstance(f, tk.Frame)])
        self.racun.configure(text=f'{total} €')
        self.after(100, self.update_gui)
