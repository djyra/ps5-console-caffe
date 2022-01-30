#! /usr/bin/env python

import tkinter as tk
from datetime import datetime, timedelta

import menu
from samsung import TV
from notifications import notify
from dialogs.receipt_dialog import ReceiptDialog
from dialogs.time_dialog import TimeDialog

class Sony(tk.Frame):
    def __init__(self,
                  master,
                  mac,
                  token,
                  port,
                  tv_ip,
                  sony,
                  color,
                  name
                  ):
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
        self.name = name

        self.TV = TV(ip=self.tv_ip,
                    port=self.port,
                    token=self.token,
                    mac=self.mac,
                    name=self.name)

        # Frame Config
        self.configure(relief='groove')
        self.configure(borderwidth="2")
        self.configure(relief="groove")

        # Widgets inside frame
        self.clock= tk.Label(self)
        self.clock.place(relx=0.034, rely=0.225, height=81, width=269)
        self.clock.configure(activebackground="#f9f9f9",
                                font="-family {Samanata} -size 24 -weight bold",
                                text='''00:00:00''')

        self.start_btn = tk.Button(self, text='START')
        self.start_btn.place(relx=0.034, rely=0.704, height=41, width=91)
        self.start_btn.configure(
                                foreground="green",
                                font="-family {Ubuntu Condensed} -size 14 -weight bold",
                                command=self.start_time,
                                cursor='hand2',
                                state='normal')

        self.add_btn = tk.Button(self, text="ADD")
        self.add_btn.place(relx=0.339, rely=0.704, height=41, width=91)
        self.add_btn.configure(
                                font="-family {Ubuntu Condensed} -size 16 -weight bold",
                                foreground="green",
                                command=self.add_time,
                                cursor='hand2',
                                state='disabled'
                                )

        self.stop_btn = tk.Button(self, text="STOP")
        self.stop_btn.place(relx=0.644, rely=0.704, height=41, width=91)
        self.stop_btn.configure(
                                font="-family {Ubuntu Condensed} -size 16 -weight bold",
                                foreground="red",
                                command=self.stop_time,
                                cursor='hand2',
                                state='disabled'
                                )

        self.booked_time_label= tk.Label(self)
        self.booked_time_label.place(relx=0.034, rely=0.507, height=21, width=250)
        self.booked_time_label.configure(activebackground="#f9f9f9", anchor='w', text='Booked time: /')

        self.ends_at_label = tk.Label(self)
        self.ends_at_label.place(relx=0.034, rely=0.592, height=21, width=250)
        self.ends_at_label.configure(activebackground="#f9f9f9",
                                    anchor='w',
                                    text='Ends at: /')


        self.sony_id_label = tk.Label(self)
        self.sony_id_label.place(relx=0.034, rely=0.028, height=54, width=64)
        self.sony_id_label.configure(
                                activebackground="#f9f9f9",
                                anchor='w',
                                font="-family {Ubuntu Condensed} -size 24 -weight bold",
                                foreground="#3EB746",
                                text=f'{self.sony_num}'
                                )

        self.menu_btn = tk.Button(self, text="MENU")
        self.menu_btn.place(relx=0.644, rely=0.028, height=41, width=91)
        self.menu_btn.configure(
                                activebackground="#5D3253",
                                font="-family {Ubuntu Condensed} -size 16 -weight bold",
                                foreground="blue",
                                command=self.open_menu,
                                cursor='hand2',
                                state='disabled'
                                )

        # initiate menu in background -> defined where fill_gui() is 
        self.menu = menu.Menu(master=self.master, sony=self)
        self.menu.fill_gui()

    def send_sony_price_to_menu(self):
        return self.time_spent

    def open_menu(self):
        self.menu.deiconify()
        self.menu.grab_set()

    def countdown(self):
        self.time_left = self.convert_seconds_left_to_time()
        self.clock['text'] = self.time_left

        if self.seconds_left:
            self.seconds_left -= 1
            self.timing_on = self.after(1000, self.countdown)

        else:
            self.timing_on = False
            self.clock.configure(foreground='red')
            self.clock['text'] = 'TIME IS UP'
            self.add_btn['state'] = 'disabled'
            # TODO: add sound 
            #self.TV.power_off()

    def start_time(self):
        if self.new_player:
            TimeDialog(sony=self,  title=f'Choose Time - Sony {self.sony_num}')
            if self.seconds_left != 0:
                self.countdown()
                self.time_spent += self.seconds_left + 1
                self.daily_usage += self.seconds_left + 1
                self.starts_at = datetime.fromtimestamp(datetime.now().timestamp())
                self.ends_at = (self.starts_at + timedelta(seconds=self.time_spent)).strftime('%H:%M:%S')
                self.booked_time_label['text'] = f'Booked time: {timedelta(seconds=self.time_spent)}'
                self.ends_at_label['text'] = f'Ends at: {self.ends_at}'
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
                self.booked_time_label['text'] = f'Booked time: /'
                self.ends_at_label['text'] = f'Ends at: /'
                self.clock['activebackground'] = 'black'
                self.clock['text'] = '00:00:00'
                self.new_player = True
                #self.TV.power_off()

    def add_time(self):
        if self.timing_on:
            self.added_time = 0
            TimeDialog(sony=self, title=f'Choose Time - Sony {self.sony_num}')

            self.time_spent += self.added_time
            self.daily_usage += self.added_time

            self.out_time = timedelta(seconds=self.time_spent)
            self.booked_time_label['text'] = f'Session time: {self.out_time}'
            self.ends_at = (self.starts_at + timedelta(seconds=self.time_spent)).strftime('%H:%M:%S')
            self.ends_at_label['text'] = f'End at: {self.ends_at}'

    def convert_seconds_left_to_time(self):
        return timedelta(seconds=self.seconds_left)
