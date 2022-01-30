#! /usr/bin/env python

import tkinter as tk
from tkinter import messagebox

from config import sonies_config
from sony_ps5 import Sony
from report import Reports
from menu import db_engine

# GUI CONFIG
def start_gui():
    root = tk.Tk(className='PS5 Timer')
    root.geometry('+250+250')
    root.title('<>< PS5 CAFFE ><>')
    root.configure(background='gray')
    root.attributes('-alpha', 1)
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='images/download.png')) # check if SVG is possible in tk

    def on_closing():
        root.withdraw()
        root.destroy()
#        if messagebox.askokcancel('Ugasi program?', 'Ako ugasis program van radnog vremena gazda ce biti obavesten.'):
#            root.destroy()
            # notify('Program ugasen u toku radnog vremena')

#    root.wm_attributes("-alpha", True)
    root.protocol('WM_DELETE_WINDOW', on_closing) # prevent accidental closing

    sony_1 = Sony(root, **sonies_config[0])
    sony_1.grid(row=0, column=0, padx=(10, 0), pady=10)

    sony_1 = Sony(root, **sonies_config[1])
    sony_1.grid(row=0, column=1, padx=(10, 0), pady=10)

    sony_1 = Sony(root, **sonies_config[2])
    sony_1.grid(row=0, column=2, padx=(10, 0), pady=10)

    sony_1 = Sony(root, **sonies_config[3])
    sony_1.grid(row=0, column=3, padx=(10, 0), pady=10)

    sony_1 = Sony(root, **sonies_config[4])
    sony_1.grid(row=1, column=1, padx=(10, 0), pady=10)

    sony_1 = Sony(root, **sonies_config[5])
    sony_1.grid(row=1, column=3, padx=(10, 0), pady=10)


    reports = Reports(root, db_engine)
    root.bind('<Shift-I>', reports.open_report)

    root.mainloop()

if __name__ == '__main__':
    try:
        start_gui()
    except Exception as e:
        print(e)
