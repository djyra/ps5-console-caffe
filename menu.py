#! /usr/bin/env python

import tkinter as tk
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, select
import datetime

from PIL import Image, ImageTk
from dialogs.receipt_dialog import ReceiptDialog
from models import Sale, Sale_item, Product

db_engine = create_engine('sqlite:///data/sales.sqlite3', echo=True)

# MenuItem Class representing a product / a snack or a drink
class MenuItem(tk.Frame):
    def __init__(self, master, price, product, image):
        tk.Frame.__init__(self, master, width=400, height=55)
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
        self.plus_btn.place(relx=0.864, rely=0.196, height=41, width=41)
        self.plus_btn.configure(cursor="fleur",
                                font="-family {Ubuntu Condensed} -size 20 -weight bold",
                                text='+',
                                command=self.add)

        self.minus_btn = tk.Button(self)
        self.minus_btn.place(relx=0.651, rely=0.196, height=41, width=41)
        self.minus_btn.configure(activebackground="#f9f9f9",
                                font="-family {Ubuntu Condensed} -size 20 -weight bold",
                                text='''-''',
                                command=self.sub)

        self.number = tk.Label(self)
        self.number.place(relx=0.762, rely=0.206, height=37, width=37)
        self.number.configure(background='white',
                                font='-family {Ubuntu Condensed} -size 16 -weight bold',
                                text=f'{self.quantity}')

        self.item_name = tk.Label(self)
        self.item_name.place(relx=0.251, rely=0.211)
        self.item_name.configure(anchor='w',
                                cursor='fleur',
                                font='-family {Ubuntu Condensed} -size 16',
                                text=f'{self.product}')

        # TODO pre-format images in PS so it executes faster, remove line below
        self.image = Image.open(self.image).transpose(Image.ROTATE_270) \
                                .resize((100, 50), Image.ANTIALIAS)
        self.ready_image = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self, image = self.ready_image)
        self.image_label.place(relx=0.00, height=50, width=100)

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
        dialog = ReceiptDialog(menu=self, title=f'Receipt for Sony {self.sony.sony_num}')
        self.after_cancel(self.updating)
        if self.sony.pay:
            with Session(db_engine) as session:
                new_sale = Sale(date_of_sale=datetime.datetime.now(),
                            total=1000)
                session.add(new_sale)

                sale_id = session.query(func.max(Sale.id)).first()[0]
                for f in self.children.values():
                    if isinstance(f, tk.Frame):
                        if f.sum > 0:
                           product_id = session.execute(select(Product.id).where(Product.name == f.product)).first()[0]
                           item_sold = Sale_item(quantity_sold=f.quantity, product_id=product_id, sale_id=sale_id) 
                           session.add(item_sold)
                session.commit()
            self.restart_menu()

    def restart_menu(self):
        for f in self.children.values():
            if isinstance(f, tk.Frame):
                f.sum = 0
                f.quantity = 0
                f.number['text'] = 0

    def show_summary(self, popup):
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
        self.koca = MenuItem(self, image='images/coca.png',
                             product='Koca 0.33',
                             price=100)
        self.koca.grid(row=0, column=0, sticky='NS')

        self.koca_light = MenuItem(self, image='images/coca-light.png',
                             product='Koca Zero 0.33',
                             price=100)
        self.koca_light.grid(row=1, column=0, sticky='NS')

        self.fanta = MenuItem(self, image='images/fanta.png',
                             product='Fanta 0.33',
                             price=100)
        self.fanta.grid(row=2, column=0, sticky='NS')

        self.sprite = MenuItem(self, image='images/sprite.png',
                             product='Sprite 0.33',
                             price=100)
        self.sprite.grid(row=3, column=0, sticky='NS')

        self.schweppes = MenuItem(self, image='images/bitter-lemon.png',
                           product='Schweppes 0.33',
                           price=100)
        self.schweppes.grid(row=4, column=0, sticky='NS')

        self.schweppes_bl = MenuItem(self, image='images/bitter-lemon.png',
                           product='Schweppes BL 0.33',
                           price=100)
        self.schweppes_bl.grid(row=5, column=0, sticky='NS')

        self.next_juice = MenuItem(self, image='images/next-orange.png',
                           product='Next orange 0.2',
                           price=115)
        self.next_juice.grid(row=6, column=0, sticky='NS')

        self.next_juice_apple = MenuItem(self, image='images/next-orange.png',
                           product='Next jabuka 0.2',
                           price=115)
        self.next_juice_apple.grid(row=7, column=0, sticky='NS')

        self.next_juice_jagoda= MenuItem(self, image='images/next-orange.png',
                           product='Next jagoda 0.2',
                           price=115)
        self.next_juice_jagoda.grid(row=8, column=0, sticky='NS')


        self.cedevita = MenuItem(self, image='images/cedevita.png',
                           product='Cedevita',
                           price=115)
        self.cedevita.grid(row=0, column=1, sticky='NS')

        self.rosa = MenuItem(self, image='images/rosa.png',
                           product='Rosa 0.33',
                           price=80)
        self.rosa.grid(row=1, column=1, sticky='NS')

        self.knjaz = MenuItem(self, image='images/knjaz.png',
                           product='Knjaz 0.25',
                           price=80)
        self.knjaz.grid(row=2, column=1, sticky='NS')

        self.heineken = MenuItem(self, image='images/heineken.png',
                           product='Heineken 0.4',
                           price=170)
        self.heineken.grid(row=3, column=1, sticky='NS')

        self.espreso = MenuItem(self, image='images/nes.png',
                           product='Espresso',
                           price=105)
        self.espreso.grid(row=4, column=1, sticky='NS')

        self.espreso_milk = MenuItem(self, image='images/nes.png',
                           product='Espresso sa mlekom',
                           price=125)
        self.espreso_milk.grid(row=5, column=1, sticky='NS')

        self.cappucino = MenuItem(self, image='images/nes.png',
                           product='Cappucino',
                           price=125)
        self.cappucino.grid(row=6, column=1, sticky='NS')

        self.akcija_1 = MenuItem(self, image='images/nes.png',
                           product='Koca + espresso',
                           price=180)
        self.akcija_1.grid(row=7, column=1, sticky='NS')


        self.akcija_2= MenuItem(self, image='images/nes.png',
                           product='Cedevita + espresso',
                           price=180)
        self.akcija_2.grid(row=8, column=1, sticky='NS')

        self.total_label = tk.Label(self, text='0',
                           font='-family {Ubuntu Condensed} -size 45 -weight bold',
                           foreground='green')
        self.total_label.grid(row=9, column=0, columnspan=2, sticky='WENS')

        self.leave_open_btn = tk.Button(self,
                   text='BACK',
                   foreground='blue',
                   font='-family {Ubuntu Condensed} -size 20 -weight bold',
                   command=self.leave_open,
                   cursor='hand2')
        self.leave_open_btn.grid(row=10, column=0, columnspan=2, sticky='NSEW')

    def update_gui(self):
        total = sum([f.sum for f in self.children.values() if isinstance(f, tk.Frame)])
        self.total_label.configure(text=f'{total} $')
        self.after(100, self.update_gui)
