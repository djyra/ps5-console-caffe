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
		self.title('DAILY REPORTS')
		self.protocol('WM_DELETE_WINDOW', self.leave_open)
		self.resizable(False, False)
		self.cal = Calendar(self, font="Arial 14", selectmode='day', locale='en_US', cursor="hand2", width=1000)

		self.cal.grid(row=0, column=0, columnspan=5, sticky="NWES")


		self.date_btn = tk.Button(self,
			text="CHOOSE THIS DATE",
			font='-weight bold',
			foreground='blue',
			command=self.show_report,
			cursor='hand2')
		self.date_btn.grid(row=1, column=0, sticky='NEWS', columnspan=5)

    # methods
	def show_report(self):
		for l in self.children.values():
			if isinstance(l, tk.Label):
				l.grid_forget()
			# header
		product_header = tk.Label(self, text='PRODUCT', font='-weight bold')
		product_header.grid(row=2, column=0)
		price_header = tk.Label(self, text='PRICE', font='-weight bold')
		price_header.grid(row=2, column=1)
		qnt_header = tk.Label(self, text='QNT.', font='-weight bold')
		qnt_header.grid(row=2, column=2)
		sum_header = tk.Label(self, text='SUM', font='-weight bold')
		sum_header.grid(row=2, column=3)

				# get that date
		date = self.cal.selection_get()
				# its local so let do it sql way who gives a fook
		sql_query = f"select product.name, product.price, sum(sale_item.quantity_sold),  sum(sale_item.quantity_sold*product.price) from product join sale_item on (product.id=sale_item.product_id) join sale on (sale_item.sale_id=sale.id) where date(sale.date_of_sale) == '{date}' group by product.id;"

		with Session(db_engine) as session:
			result = session.execute(sql_query).all()

		if len(result) == 0:
			empty_label = tk.Label(self, text='NO SALES FOR THIS DAY')
			empty_label.grid(row=2, column=0, columnspan=5, sticky='NEWS')

		# render table 
		for i, res in enumerate(result):
			for idx, r in enumerate(res):
				record = tk.Label(self, text=r)
				record.grid(row=i+3, column=idx)

	def open_report(self, event):
		pw = tk.simpledialog.askstring('REPORTS', 'Enter admin password:', show='*')
		if pw == 'itslocal':
			self.deiconify()
			self.grab_set()

	def leave_open(self):
		self.grab_release()
		self.withdraw()
