#! /usr/bin/env python

import datetime
import tkinter as tk
from tkinter import simpledialog


# project imports
import menu
from notifications import notify
from samsung import TV
import threading
import database


class Sony(tk.Frame):
    def __init__(self, master, mac, token, port, tv_ip, sony, color):
     
        tk.Frame.__init__(self, master, width=300, height=300)

        # Logic
        self.master = master
        self.sony = sony
        self.seconds_left = 0
        self.timing_on = False
        self.pause_seconds = 0
        self.time_spent = 0
        self.daily_usage = 0
        self.new_player = False
        self.igrac = 0

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

        # Widgets
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
                                text='''START''',
                                command=self.start_time,
                                cursor='hand2',
                                state='disabled')

        self.add_btn = tk.Button(self)
        self.add_btn.place(relx=0.339, rely=0.704, height=41, width=91)
        self.add_btn.configure(activebackground="white",
                                background="#1ad82d",
                                font="-family {Ubuntu Condensed} -size 14 -weight bold",
                                foreground="white",
                                text='''ADD TIME''',
                                command=self.add_time,
                                cursor='hand2',
                                state='disabled')

        self.stop_btn = tk.Button(self)
        self.stop_btn.place(relx=0.644, rely=0.704, height=41, width=91)
        self.stop_btn.configure(activebackground="white",
                                background="red",
                                font="-family {Ubuntu Condensed} -size 14 -weight bold",
                                foreground="white",
                                text='''STOP''',
                                command=self.stop_time,
                                cursor='hand2',
                                state='disabled')

        self.novi_igrac_btn = tk.Button(self)
        self.novi_igrac_btn.place(relx=0.644, rely=0.845, height=41, width=91)
        self.novi_igrac_btn.configure(activebackground="#f9f9f9",
                                    background="#0007d8",
                                    font="-family {Ubuntu Condensed} -size 10 -weight bold",
                                    foreground="white",
                                    text='''NEW SESSION''',
                                    command=self.novi_igrac,
                                    cursor='hand2')


        self.vreme_igrac_label = tk.Label(self)
        self.vreme_igrac_label.place(relx=0.034, rely=0.507, height=21, width=250)
        self.vreme_igrac_label.configure(activebackground="#f9f9f9",
                                        anchor='w',
                                        text='Session time: /')


        self.ceo_dan_label = tk.Label(self)
        self.ceo_dan_label.place(relx=0.034, rely=0.592, height=21, width=250)
        self.ceo_dan_label.configure(activebackground="#f9f9f9",
                                    anchor='w',
                                    text='Total time for today: /')


        self.broj_sony = tk.Label(self)
        self.broj_sony.place(relx=0.034, rely=0.028, height=54, width=64)
        self.broj_sony.configure(activebackground="#f9f9f9",
                                anchor='w',
                                font="-family {Ubuntu Condensed} -size 24 -weight bold",
                                foreground="green",
                                text=f'{self.sony}')


        self.igrac_label = tk.Label(self)
        self.igrac_label.place(relx=0.034, rely=0.901, height=21, width=169)
        self.igrac_label.configure(anchor='w',
                                   text='''Session number: 0''')


        self.pice_btn = tk.Button(self)
        self.pice_btn.place(relx=0.644, rely=0.028, height=41, width=91)
        self.pice_btn.configure(activebackground="white",
                                background="orange",
                                font="-family {Ubuntu Condensed} -size 14 -weight bold",
                                foreground="white",
                                text='MENU',
                                command=self.open_pice,
                                cursor='hand2'
                                ) # state='disabled'

        self.new_window = tk.Toplevel(self.master)
        menu.start_gui(self.new_window)



    # LOGIC
    def open_pice(self):
        self.new_window.deiconify()
        self.new_window.grab_set()

    def countdown(self):
        self.time_left = self.convert_seconds_left_to_time()
        self.sat_label['text'] = self.time_left
        self.novi_igrac_btn['state'] = 'disabled'

        if self.seconds_left:
            self.seconds_left -= 1
            self.timing_on = self.after(1000, self.countdown)

        else:
            self.timing_on = False
            self.sat_label.configure(foreground='red')
            self.sat_label['text'] = '00:00:00'
            self.add_btn['state'] = 'disabled'
            self.stop_btn['state'] = 'disabled'
            self.start_btn['state'] = 'disabled'
            self.novi_igrac_btn['state'] = 'normal'
            self.TV.power_off()
    

    def start_time(self):
        try:
            if self.new_player:
                self.seconds_left = simpledialog.askinteger(title='SESSION DURATION', prompt='M I N U T E S') * 60
                try:
                    self.TV.power_on() 
                    self.stop_time()
                    self.countdown()
                    self.time_spent += self.seconds_left + 1
                    self.daily_usage += self.seconds_left + 1
                    self.out_time = datetime.timedelta(seconds=self.time_spent)
                    self.vreme_igrac_label['text'] = f'Sessnion time: {self.out_time}'
                    self.out_time2 = datetime.timedelta(seconds=self.daily_usage)
                    self.ceo_dan_label['text'] = f'Total time for today: {self.out_time2}'
                    self.new_player = False
                    self.start_btn['state'] = 'disabled'
                    self.stop_btn['state'] = 'normal'
                    self.add_btn['state'] = 'normal'
                    database.insert(time=datetime.datetime.now(), sony=self.sony, time_booked=self.time_spent)

                    message = u'\U0001F3AE' + ' Sony ' + str(self.sony) + u' \n\U000023F0 '  + str(self.out_time)
                    # notify(message)
                except Exception as e:
                    print('start_time() 2nd loop bug', e)
                    self.start_time()

        except Exception as e:
            print('start_time() bug:', e)
            self.sat_label['text'] = 'Enter time'

    def recover_start_btn(self):
        self.start_btn.place(relx=0.034, rely=0.704, height=41, width=91)
        self.start_btn['state'] = 'disabled'
        self.novi_igrac_btn['state'] = 'normal'
        self.sat_label['text'] = '00:00:00'

    def stop_time(self):
        try:
            if self.timing_on:
                self.msg = tk.messagebox.askquestion('SHUT DOWN', 'You you really want to turn of TV?', icon='warning')
                if self.msg == 'yes':
                    self.after_cancel(self.timing_on)
                    self.timing_on = False
                    self.start_btn.place_forget()
                    self.stop_btn['state'] = 'disabled'
                    self.add_btn['state'] = 'disabled'
                    self.novi_igrac_btn['state'] = 'disabled'
                    self.TV.power_off()
                    self.sat_label['text'] = 'STOPIRANO'
                    self.master.after(20000, self.recover_start_btn)
                else:
                    pass
        except Exception as e:
            print('stop_time() bug:', e)
            
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


    def novi_igrac(self):

        self.msg = tk.messagebox.askquestion('NEW SESSION', 'Start a new session?', icon='info')
        if self.msg == 'yes':
            self.stop_time()
            self.new_player = True
            self.igrac += 1
            self.time_spent = 0
            self.seconds_left = 0
            self.vreme_igrac_label['text'] = 'Restarted - New Session'
            self.igrac_label['text'] = f'Session number: {self.igrac}'
            self.start_btn['state'] = 'normal'
            print(self.seconds_left)
            if self.seconds_left == 0:
                self.stop_btn['state'] = 'disabled'
                self.add_btn['state'] = 'disabled'

            self.pice_btn['state'] = 'normal'
            self.sat_label['foreground'] = 'black'
        else:
            pass

    # def restart_all(self):
    #     self.stop_time()
    #     self.description['text'] = 'Ukupno vreme igrac: /'
    #     self.description2['text'] = 'Ukupno vreme za danas: /'
    #     self.time_spent = 0
    #     self.seconds_left = 0
    #     self.daily_usage = 0
    #     self.igrac = 1
    #     self.description3['text'] = f'Broj Igraca za danas: /'


    def convert_seconds_left_to_time(self):
        return datetime.timedelta(seconds=self.seconds_left)