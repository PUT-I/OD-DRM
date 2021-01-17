from poke_visor.gui.pokevisor_image_ui import main
from poke_visor import *
from serial_key_generator import key_validator as kv
from serial_key_generator import key_utils
from tkinter import *
from tkinter import messagebox
import os
# Designing Main(first) window
def validate():
    key1=key_entry.get()
    if(kv.check_key(key1)==kv.Key.GOOD):
        main()
    else:
        messagebox.showinfo("error", "Wrong key")
    return True
    
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    global key
    global key_entry
    
    key = StringVar()
 
    Label(main_screen, text="Please enter your serial key below", bg="blue").pack()
    Label(main_screen, text="").pack()
    key_lable = Label(main_screen, text="key * ")
    key_lable.pack()
    key_entry = Entry(main_screen, textvariable=key)
    key_entry.pack()
    Label(main_screen, text="").pack()
    Button(main_screen, text="Register", width=10, height=1, bg="blue", command = validate).pack()
 
    main_screen.mainloop()
 
 
main_account_screen()
