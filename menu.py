#! /usr/bin/env python

import tkinter as tk
from PIL import Image, ImageTk


# Menu item class that can be reused for any product

class MenuItem(tk.Frame):
    def __init__(self, master, price, product, image):
        tk.Frame.__init__(self, master, width=675, height=95)
        # tk.Frame.__init__(self, master, width=300, height=300)
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
                                font='-family {Ubuntu Condensed} -size 24 -weight bold',
                                text=f'{self.quantity}')

        self.item_name = tk.Label(self)
        self.item_name.place(relx=0.311, rely=0.211, height=61, width=229)
        self.item_name.configure(anchor='w',
                                cursor='fleur',
                                font='-family {Ubuntu Condensed} -size 24',
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
            print(self.sum)

    def sub(self):
        if self.quantity >= 1: # can't go negative
            self.quantity -= 1
            self.number['text'] = str(self.quantity)
            self.sum -= self.price
            print(self.sum)


### INITIATE GUI

def start_gui(window):




    # Commands for buttons
    def show_summary():
        summary = []
        for f in window.children.values():
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
            string += s['product'] + ': ' + s['quantity'] + ' x ' + s['price'] + ' = ' + s['sum'] + '\n'
            suma += float(s['sum'])

        result = string + 'Total: \t\t' + str(suma)
        print(result)
        return result

    def opened_order():
        window.grab_release() # remove grab and withdraws window
        window.withdraw()

    def pay_cash():
        window.focus()
        msg = tk.messagebox.askquestion('CHARGE?', f'{show_summary()}', icon='info', parent=item3)
        # in above dialog parent must be any frame inside the window so it will appear on the top

        # add to database # TODO


        if msg == 'yes': # after paying restart all values
            window.grab_release()
            window.after_cancel(ok)
            window.withdraw()
            for f in window.children.values(): # iterating over frames and its values / each frame represents one Menu Item
                if isinstance(f, tk.Frame):
                    f.sum = 0
                    f.quantity = 0
                    f.number['text'] = 0
        else:
            pass
    

    # WINDOW CONFIG
    window.withdraw() # invisible when initiated
    window.geometry('675x700+250+250')
    window.title('<>< Snacks and Drinks ><>')
    window.resizable(False,False)
    window.wm_attributes("-topmost", True)
    window.protocol('WM_DELETE_WINDOW', opened_order)
    window.transient(window.master) # removes min/max


    # MENU ITEMS
    item1 = MenuItem(window, image='images/coca.png',
                            product='Koca 0.5',
                            price=3.5)
    item1.grid(row=0, column=0, sticky='NWES')

    item2 = MenuItem(window, image='images/fanta.png',
                            product='Fanta 0.5',
                            price=3.5)
    item2.grid(row=1, column=0, sticky='NWES')

    item3 = MenuItem(window, image='images/sprite.png',
                            product='Sprite 0.5',
                            price=3.5)
    item3.grid(row=2, column=0, sticky='NWES')

    item4 = MenuItem(window, image='images/heineken.png',
                            product='Heineken 0.33',
                            price=4)
    item4.grid(row=3, column=0, sticky='NWES')

    item5 = MenuItem(window, image='images/sandwich.png',
                            product='Sandwich',
                            price=5)
    item5.grid(row=4, column=0, sticky='NWES')


    racun = tk.Label(window, text='0',
                            font='-family {Ubuntu Condensed} -size 45 -weight bold',
                            foreground='green')
    racun.grid(row=5, column=0, sticky='NSEW')
  
    open_tab = tk.Button(window,
                    text='OPEN TAB',
                    background='blue',
                    foreground='white',
                    font='-family {Ubuntu Condensed} -size 20 -weight bold',
                    command=opened_order,
                    cursor='hand2')
    open_tab.grid(row=6, column=0, sticky='NSEW')


    pay = tk.Button(window,
                    text='CHARGE',
                    background='red',
                    foreground='white',
                    font='-family {Ubuntu Condensed} -size 20 -weight bold',
                    command=pay_cash,
                    cursor='hand2')
    pay.grid(row=7, column=0, sticky='NSEW')

    
    def make_sum():
        suma = sum([f.sum for f in window.children.values() if isinstance(f, tk.Frame)])
        racun.configure(text= f'{suma} €')
        window.after(100, make_sum)

    ok = window.after(100, make_sum) # has to be done like this so it can be canceled in pay_cash()


