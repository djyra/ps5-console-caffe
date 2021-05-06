#! /usr/bin/env python

from datetime import datetime, timedelta
import tkinter as tk
from tkinter import simpledialog, messagebox

from notifications import notify
from samsung import TV
import menu
from dialogs import ReceiptDialog, TimeDialog

class Sony(tk.Frame):
    def __init__(self, master, mac, token, port, tv_ip, sony, color):
        tk.Frame.__init__(self, master, width=300, height=300)

        # Logic
        self.master = master
        self.sony_num = sony
        self.seconds_left = 0
        self.timing_on = False
        self.time_spent = 0
        self.daily_usage = 0
        self.added_time = 0
        self.new_player = True 
        self.igrac = 0
        self.price = []
        self.pay = False

        # TV Settings
        self.tv_ip = tv_ip
        self.mac = mac
        self.token = token
        self.port = port
        self.color = color

        self.TV = TV(ip=self.tv_ip,
                    port=self.port,
                    token=self.token,
                    mac=self.mac)

        # Frame Config
        self.configure(relief='groove')
        self.configure(borderwidth="2")
        self.configure(relief="groove")

        # Widgets inside frame
        self.sat_label = tk.Label(self)
        self.sat_label.place(relx=0.034, rely=0.225, height=81, width=269)
        self.sat_label.configure(activebackground="#f9f9f9",
                                font="-family {Samanata} -size 24 -weight bold",
                                text='''00:00:00''')

        self.start_btn = tk.Button(self)
        self.start_btn.place(relx=0.034, rely=0.704, height=41, width=91)
        self.start_btn.configure(activebackground="white",
                                background="#1ad82d",
                                font="-family {Ubuntu Condensed} -size 14 -weight bold",
                                foreground="white",
                                text='START',
                                command=self.start_time,
                                cursor='hand2',
                                state='normal')

        self.add_btn = tk.Button(self)
        self.add_btn.place(relx=0.339, rely=0.704, height=41, width=91)
        self.add_btn.configure(activebackground="white",
                                background="#1ad82d",
                                font="-family {Ubuntu Condensed} -size 14 -weight bold",
                                foreground="white",
                                text='DODAJ',
                                command=self.add_time,
                                cursor='hand2',
                                state='disabled')

        self.stop_btn = tk.Button(self)
        self.stop_btn.place(relx=0.644, rely=0.704, height=41, width=91)
        self.stop_btn.configure(activebackground="white",
                                background="red",
                                font="-family {Ubuntu Condensed} -size 14 -weight bold",
                                foreground="white",
                                text='STOP',
                                command=self.stop_time,
                                cursor='hand2',
                                state='disabled')

        self.vreme_igrac_label = tk.Label(self)
        self.vreme_igrac_label.place(relx=0.034, rely=0.507, height=21, width=250)
        self.vreme_igrac_label.configure(activebackground="#f9f9f9", anchor='w', text='Bookirano vreme: /') 

        self.ends_at_label = tk.Label(self)
        self.ends_at_label.place(relx=0.034, rely=0.592, height=21, width=250)
        self.ends_at_label.configure(activebackground="#f9f9f9",
                                    anchor='w',
                                    text='Kraj u: /')


        self.broj_sony = tk.Label(self)
        self.broj_sony.place(relx=0.034, rely=0.028, height=54, width=64)
        self.broj_sony.configure(activebackground="#f9f9f9",
                                anchor='w',
                                font="-family {Ubuntu Condensed} -size 24 -weight bold",
                                foreground="green",
                                text=f'{self.sony_num}')

        self.menu_btn = tk.Button(self)
        self.menu_btn.place(relx=0.644, rely=0.028, height=41, width=91)
        self.menu_btn.configure(activebackground="white",
                                background="orange",
                                font="-family {Ubuntu Condensed} -size 14 -weight bold",
                                foreground="white",
                                text='MENU',
                                command=self.open_menu,
                                cursor='hand2',
                                state='disabled'
                                )

        self.menu = menu.Menu(master=self.master, sony=self)
        self.menu.fill_gui()

    def send_sony_price_to_menu(self):
        return self.time_spent

    def open_menu(self):
        self.menu.deiconify()
        self.menu.grab_set()

    def countdown(self):
        self.time_left = self.convert_seconds_left_to_time()
        self.sat_label['text'] = self.time_left

        if self.seconds_left:
            self.seconds_left -= 1
            self.timing_on = self.after(1000, self.countdown)

        else:
            self.timing_on = False
            self.sat_label.configure(foreground='red')
            self.sat_label['text'] = 'VREME ISTEKLO'
            self.add_btn['state'] = 'disabled'
            #self.TV.power_off()

    def start_time(self):
        if self.new_player:
            TimeDialog(sony=self,  title='Izaberi Vreme')
            if self.seconds_left != 0:
                self.countdown()
                self.time_spent += self.seconds_left + 1
                self.daily_usage += self.seconds_left + 1
                self.starts_at = datetime.fromtimestamp(datetime.now().timestamp())
                self.ends_at = (self.starts_at + timedelta(seconds=self.time_spent)).strftime('%H:%M:%S')
                self.vreme_igrac_label['text'] = f'Bookirano vreme: {timedelta(seconds=self.time_spent)}'
                self.ends_at_label['text'] = f'Kraj u: {self.ends_at}'
                self.new_player = False
                self.start_btn['state'] = 'disabled'
                self.stop_btn['state'] = 'normal'
                self.add_btn['state'] = 'normal'
                self.menu_btn['state'] = 'normal'

    def stop_time(self):
        if self.timing_on:
            self.menu.pay_cash()
            if self.pay:
                self.price = []
                self.pay = False
                self.after_cancel(self.timing_on)
                self.seconds_left = 0
                self.time_spent = 0
                self.start_btn['state'] = 'normal'
                self.stop_btn['state'] = 'disabled'
                self.add_btn['state'] = 'disabled'
                self.menu_btn['state'] = 'disabled'
                self.vreme_igrac_label['text'] = f'Bookirano vreme: /'
                self.ends_at_label['text'] = f'Kraj u: /'
                self.sat_label['activebackground'] = 'black'
                self.sat_label['text'] = '00:00:00'
                self.new_player = True
                #self.TV.power_off()

    def add_time(self):
        if self.timing_on:
            self.added_time = 0 
            TimeDialog(sony=self, title='Izaberi Vreme')

            self.time_spent += self.added_time
            self.daily_usage += self.added_time

            self.out_time = timedelta(seconds=self.time_spent)
            self.vreme_igrac_label['text'] = f'Session time: {self.out_time}'
            self.ends_at = (self.starts_at + timedelta(seconds=self.time_spent)).strftime('%H:%M:%S')
            self.ends_at_label['text'] = f'Kraj u: {self.ends_at}'

    def convert_seconds_left_to_time(self):
        return timedelta(seconds=self.seconds_left)



