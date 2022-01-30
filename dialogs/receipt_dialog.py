import tkinter as tk
import tkinter.simpledialog

class ReceiptDialog(tkinter.simpledialog.Dialog):
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

        inner_frame = tk.Frame(self)
        inner_frame.pack()
        artikel = tk.Label(inner_frame, text='PRODUCTS')
        artikel.grid()
        cena = tk.Label(inner_frame, text='PRICE')
        cena.grid(row=0, column=1, padx=5, pady=5)
        kolicina = tk.Label(inner_frame, text='QNT.')
        kolicina.grid(row=0, column=2)
        ukupno = tk.Label(inner_frame, text='SUM')
        ukupno.grid(row=0, column=3)

        for i, s in enumerate(summary, 1):
            for idx, value in enumerate(s.values()):
                val_lab = tk.Label(inner_frame, text=value)
                if i == 0:
                    val_lab['anchor'] = 'w'
                val_lab.grid(row=i, column=idx)

        sony_price = self.sony.price
        start = len(summary)
        for i in sony_price:
            sony_lab = tk.Label(inner_frame, text='SONY')
            sony_lab.grid(row=start+1, column=0)
            sony_price = tk.Label(inner_frame, text=i)
            sony_price.grid(row=start+1, column=3)
            start += 1


        total = sum([int(x['sum']) for x in summary]) + sum(self.menu.sony.price)
        total_lab = tk.Label(inner_frame, text=total, font='-weight bold -size 15')
        total_lab.grid(column=3)

        pay_btn = tk.Button(inner_frame, text='CHARGE', command=self.pay, foreground='green')
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

