#! /usr/bin/env python

from sony_ps5 import Sony
from config import sonies_config
import tkinter as tk


# GUI CONFIG

def start_gui():
    root = tk.Tk()
    root.geometry('+250+250')
    root.title('<>< eSPORTS CAFFE ><>')
    root.configure(background='gray')

    def on_closing():
        if tk.messagebox.askokcancel('Shutdown', 'Do you really want to quit??\n The boss will be notified.'):
            root.destroy()
            # notify('Program ugasen u toku radnog vremena')

    root.wm_attributes("-alpha", True)
    root.protocol('WM_DELETE_WINDOW', on_closing) # prevent accidental closing

    sony_1 = Sony(root, **sonies_config[0])
    sony_1.grid()

    sony_2 = Sony(root, **sonies_config[1])
    sony_2.grid(row=0, column=1)

    sony_3 = Sony(root, **sonies_config[2])
    sony_3.grid(row=0, column=2)

    sony_4 = Sony(root, **sonies_config[3])
    sony_4.grid(row=0, column=3)

    sony_5 = Sony(root, **sonies_config[4])
    sony_5.grid(row=1, column=1, padx=20, pady=20)

    sony_6 = Sony(root, **sonies_config[5])
    sony_6.grid(row=1, column=3, padx=20)

    root.mainloop()


if __name__ == '__main__':
    try:
        start_gui()
    except Exception as e:
        print(e)