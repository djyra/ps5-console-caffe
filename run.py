#! /usr/bin/env python

import tkinter as tk
from tkinter import messagebox

from sony_ps5 import Sony
from config import sonies_config

# GUI CONFIG
def start_gui():
    root = tk.Tk()
    root.geometry('+250+250')
    root.title('<>< RELAX IGRAONICA ><>')
    root.configure(background='gray')

    def on_closing():
        if messagebox.askokcancel('Ugasi program?', 'Ako ugasis program van radnog vremena gazda ce biti obavesten.'):
            root.destroy()
            # notify('Program ugasen u toku radnog vremena')

    root.wm_attributes("-alpha", True)
    root.protocol('WM_DELETE_WINDOW', on_closing) # prevent accidental closing

    sony_1 = Sony(root, **sonies_config[0])
    sony_1.grid(padx=(10, 0), pady=10)

    sony_2 = Sony(root, **sonies_config[1])
    sony_2.grid(row=0, column=1, padx=10)

    sony_3 = Sony(root, **sonies_config[2])
    sony_3.grid(row=0, column=2, padx=0)

    sony_4 = Sony(root, **sonies_config[3])
    sony_4.grid(row=0, column=3, padx=10)

    sony_5 = Sony(root, **sonies_config[4])
    sony_5.grid(row=1, column=1, pady=(20, 10))

    sony_6 = Sony(root, **sonies_config[5])
    sony_6.grid(row=1, column=3, padx=10)

    root.mainloop()


if __name__ == '__main__':
    try:
        start_gui()
    except Exception as e:
        print(e)
