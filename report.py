#! /usr/bin/env python

import tkinter as tk
import tkinter.simpledialog
from tkcalendar import Calendar
from sqlalchemy.orm import Session
from menu import db_engine

class Reports(tk.Toplevel):
	def __init__(self, master, dbengine):
		tk.Toplevel.__init__(self, master)
		self.master = master
		self.dbengine = dbengine
		self.withdraw()
		self.title('IZVESTAJI')
		self.protocol('WM_DELETE_WINDOW', self.leave_open)
		self.resizable(False, False)

		self.cal = Calendar(self,
				font="Arial 14",
				selectmode='day',
				locale='en_US',
				cursor="hand2",
				width=1000)
		self.cal.grid(row=0, column=0, columnspan=5, sticky='NWES')
		self.date_btn = tk.Button(self, text="IZABERI DATUM", font='-weight bold', background='green', foreground='white',  command=self.show_report, cursor='hand2')
		self.date_btn.grid(row=1, column=0, sticky='NEWS', columnspan=5)

	def show_report(self):
		for l in self.children.values():
			if isinstance(l, tk.Label):
				l.grid_forget()
		artikal = tk.Label(self, text='ARTIKAL', font='-weight bold')
		artikal.grid(row=2, column=0)
		cena = tk.Label(self, text='CENA', font='-weight bold')
		cena.grid(row=2, column=1)
		kol = tk.Label(self, text='KOL.', font='-weight bold')
		kol.grid(row=2, column=2)
		ukupno = tk.Label(self, text='UKUPNO', font='-weight bold')
		ukupno.grid(row=2, column=3)
		datum = self.cal.selection_get()
		sql_query = f"select product.name, product.price, sum(sale_item.quantity_sold),  sum(sale_item.quantity_sold*product.price) from product join sale_item on (product.id=sale_item.product_id) join sale on (sale_item.sale_id=sale.id) where date(sale.date_of_sale) == '{datum}' group by product.id;"
		with Session(db_engine) as session:
			result = session.execute(sql_query).all()
		if len(result) == 0:
			empty_label = tk.Label(self, text='NEMA PODATAKA ZA OVAJ DAN')
			empty_label.grid(row=2, column=0, columnspan=5, sticky='NEWS')
		for i, res in enumerate(result):
			for idx, r in enumerate(res):
				record = tk.Label(self, text=r)
				record.grid(row=i+3, column=idx)

	def open_report(self, event):
		pw = tk.simpledialog.askstring('IZVESTAJI', 'Unesi sifru:', show='*')
		if pw == 'lakiadmin':
			self.deiconify()
			self.grab_set()

	def leave_open(self):
		self.grab_release() # remove grab and withdraw window
		self.withdraw()


