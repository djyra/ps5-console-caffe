#! /usr/bin/env python
# standalone remote that can control all sonises - only sound needed

import tkinter as tk
from samsungtvws import SamsungTVWS
from config import sonies_config

class Remote(tk.Frame):
	def __init__(self, master, tv_ip, port, token, sony, color, mac, name):

		tk.Frame.__init__(self, master, width=200, height=200)

        self.name = name
		self.master = master
		self.tv_ip = tv_ip
		self.port = port
		self.token = token
		self.master = master
		self.sony = sony
		self.color = color
		self.mac = mac

        self.tv = SamsungTVWS(host=self.tv_ip,port=self.port,token=self.token,name='Testing',timeout=60)

		self.plus_btn = tk.Button(self,
								text='+',
								font='-size 25',
								command=self.vol_up,
								width=3, height=2,
								state='disabled',
								background=self.color)
		self.plus_btn.grid(row=1, column=0, sticky='NWES')

		self.minus_btn = tk.Button(self,
								text='-',
								font='-size 25',
								command=self.vol_down,
								width=3, height=2,
								state='disabled',
								background=self.color)
		self.minus_btn.grid(row=1, column=1)


		self.ctrl_btn = tk.Button(self,
								text=f'{self.sony}.Connect',
								background=self.color,
								font='-size 25',
								command=self.connect,
								cursor='hand2')

		self.ctrl_btn.grid(row=0, column=0, columnspan=2, sticky='NWES')


	def control(self):
		self.minus_btn['state'] = 'disabled'
		self.plus_btn['state'] = 'disabled'
		self.ctrl_btn['state'] = 'normal'

	def connect(self):
		self.tv.open()
		self.minus_btn['state'] = 'normal'
		self.plus_btn['state'] = 'normal'
		self.ctrl_btn['state'] = 'disabled'
		self.after(60000, self.control)

	def vol_up(self):
		self.tv.shortcuts().volume_up()

	def vol_down(self):
		self.tv.shortcuts().volume_down()

# initiate the multi remote
root = tk.Tk()
root.title('Remote Controllers')
root.resizable(0,0)

remote1 = Remote(root, **sonies_config[0])
remote1.grid(row=0, column=1)

remote2 = Remote(root, **sonies_config[1])
remote2.grid(row=1, column=1)

remote3 = Remote(root, **sonies_config[2])
remote3.grid(row=2, column=1)

remote4 = Remote(root, **sonies_config[3])
remote4.grid(row=3, column=1)

remote5 = Remote(root, **sonies_config[4])
remote5.grid(row=4, column=1)

remote6 = Remote(root, **sonies_config[5])
remote6.grid(row=5, column=1)

# run
root.mainloop()
