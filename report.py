#! /usr/bin/env python

import sqlite3
import tkinter as tk
from tkcalendar import Calendar


class Table(tk.Frame):
	def __init__(self, master, datum):
		tk.Frame.__init__(self, master)
		self.mater = master
		self.datum = datum
		self.headers = ('SONY', 'START', 'BOOKED')

	def gimme_all(self):
		with sqlite3.connect('data/db.sqlite3') as self.conn:
			self.cur = self.conn.cursor()
			self.cur.execute("SELECT sony, time(time_started), time_booked / 60 / 60 + 'h' from ps_time where date(time_started) = ? order by time(time_started)", (self.datum, ))
			self.res = self.cur.fetchall()
			if self.res:
				self.cur.execute('SELECT sum(time_booked / 60 / 60) from ps_time where date(time_started) = ?', (self.datum,))
				self.r = self.cur.fetchone()
				self.r = ('','-------->',round(self.r[0], 2))
				self.res.append(self.r)
				return self.res
			else:
				self.label = tk.Label(self.master, text='No entries for this day')
				self.label.grid(row=3, column=0)

	def create_table(self):

		if self.gimme_all():

			for i in range(3):
				self.header = tk.Label(self,width=9,
										fg='blue',
										font=('Arial', 16),
										relief=tk.RAISED)
				self.header.grid(row=0, column=i)
				self.header['text'] = self.headers[i]

			for i in range(len(self.gimme_all())):
				for j in range(len(self.gimme_all()[0])):

					self.e = tk.Label(self, width=9,
											fg='black',
											font=('Arial', 16),
											relief=tk.RAISED)
					self.e.grid(row=i+1, column=j)

					if isinstance(self.gimme_all()[i][j], float):
						self.e['text'] = round(self.gimme_all()[i][j], 2)
					else:
						self.e['text'] = self.gimme_all()[i][j]


root = tk.Tk()
cal = Calendar(root, font="Arial 14", selectmode='day', locale='en_US',
	                   cursor="hand2")

cal.grid(row=0, column=0)


def show_report():
	datum = cal.selection_get()
	t = Table(root, datum=datum)
	t.create_table()
	label = tk.Label(root, text=datum)
	label.grid(row=2, column=0)
	t.grid(row=3, column=0, sticky='NWES')
	root.update()


date_btn = tk.Button(root, text="-> CHOOSE DATE <-", font='-weight bold', command=show_report, cursor='hand2')
date_btn.grid(row=1, column=0)