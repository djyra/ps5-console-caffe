#! /usr/bin/env python

import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

from notifications import notify
from samsung import TV
import utils
import database
import menu

class Sony(tk.Frame):
    def __init__(self, master, mac, token, port, tv_ip, sony, color):

        tk.Frame.__init__(self, master, width=300, height=300)

        # Logic
        self.master = master
        self.sony = sony
        self.seconds_left = 0
        self.timing_on = False
        self.time_spent = 0
        self.daily_usage = 0
        self.new_player = True 
        self.igrac = 0
        self.price = 0

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
        self.ceo_dan_label = tk.Label(self)
        self.ceo_dan_label.place(relx=0.034, rely=0.592, height=21, width=250)
        self.ceo_dan_label.configure(activebackground="#f9f9f9",
                                    anchor='w',
                                    text='Ukupno vreme za danas: /')


        self.broj_sony = tk.Label(self)
        self.broj_sony.place(relx=0.034, rely=0.028, height=54, width=64)
        self.broj_sony.configure(activebackground="#f9f9f9",
                                anchor='w',
                                font="-family {Ubuntu Condensed} -size 24 -weight bold",
                                foreground="green",
                                text=f'{self.sony}')

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

    # LOGIC
    def open_menu(self):
        self.menu.deiconify()

    def open_pice(self):
        self.new_window.deiconify()
        self.new_window.grab_set()

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
            self.stop_btn['state'] = 'disabled'
            self.start_btn['state'] = 'normal'
            #self.TV.power_off()

    def start_time(self):
        if self.new_player:
            #TODO make custom dialog to choose from 1, 2, 3 hours
#            self.seconds_left = simpledialog.askinteger(title='SESSION DURATION', prompt='M I N U T E S') * 60
            utils.TimeDialog(master=self.master, sony=self, title='Izaberi Vreme')
            if self.seconds_left != 0:
                self.countdown()
                self.time_spent += self.seconds_left + 1
                self.daily_usage += self.seconds_left + 1
                self.vreme_igrac_label['text'] = f'Bookirano vreme: {datetime.timedelta(seconds=self.time_spent)}'
                self.ceo_dan_label['text'] = f'Ukupno vreme za danas: {datetime.timedelta(seconds=self.daily_usage)}'
                self.new_player = False
                self.start_btn['state'] = 'disabled'
                self.stop_btn['state'] = 'normal'
                self.add_btn['state'] = 'normal'
                self.menu_btn['state'] = 'normal'

        else:
            self.sat_label['text'] = 'Enter time'

    def stop_time(self):
        if self.timing_on:
            self.msg = messagebox.askquestion('Zavrsi seshn?', 'Sigurno? Naplati racun', icon='warning')
            if self.msg == 'yes':
                self.after_cancel(self.timing_on)
                self.seconds_left = 0
                self.time_spent = 0
                self.start_btn['state'] = 'normal'
                self.stop_btn['state'] = 'disabled'
                self.add_btn['state'] = 'disabled'
                #self.TV.power_off()
                self.vreme_igrac_label['text'] = f'Bookirano vreme: /'
                self.sat_label['text'] = '00:00:00'
                self.new_player = True
                self.menu.pay_cash()
            else:
                pass

    def add_time(self):
        if self.timing_on:
            try:
                self.added_time = simpledialog.askinteger(title='ADD TIME', prompt='Insert additional time in MINUTES') * 60
                self.seconds_left += self.added_time
                self.time_spent += self.added_time
                self.daily_usage += self.added_time

                self.out_time = datetime.timedelta(seconds=self.time_spent)
                self.vreme_igrac_label['text'] = f'Session time: {self.out_time}'

                self.out_time2 = datetime.timedelta(seconds=self.daily_usage)
                self.ceo_dan_label['text'] = f'Total time for today {self.out_time2}'
            except Exception as e:

                print(e)
    def convert_seconds_left_to_time(self):
        return datetime.timedelta(seconds=self.seconds_left)
