from poke_visor.gui.chip_classifier_generator_ui import main  as chip_main
from poke_visor.gui.pokevisor_image_ui import main  as image_main
from poke_visor.gui.pokevisor_video_ui import main  as video_main
from serial_key_generator import key_validator as kv
from serial_key_generator import key_utils
from tkinter import *
from tkinter import messagebox
import os
# Designing Main(first) window
def validate():
    key1=key_entry.get()
    if(kv.check_key(key1)==kv.Key.GOOD):
        main_screen.destroy()
        openNewWindow()
        
    else:
        messagebox.showinfo("error", "Wrong key")
    return True

def pokevisor_image_ui_start():
    newWindow.destroy()
    image_main()
    openNewWindow()

def chip_classifier_generator_ui_start():
    newWindow.destroy()
    chip_main()
    openNewWindow()


def pokevisor_video_ui_start():
    newWindow.destroy()
    video_main()
    openNewWindow()

def openNewWindow(): 
      
    # Toplevel object which will  
    # be treated as a new window 
    global newWindow
    newWindow = Tk()
  
    # sets the title of the 
    # Toplevel widget 
    newWindow.title("New Window") 
  
    # sets the geometry of toplevel 
    newWindow.geometry("200x200") 
    Button(newWindow, text="chip_classifier_generator_ui", width=10, height=1, bg="blue", command = chip_classifier_generator_ui_start).pack()
    Button(newWindow, text="pokevisor_image_ui", width=10, height=1, bg="blue", command = pokevisor_image_ui_start).pack()
    Button(newWindow, text="pokevisor_video_ui", width=10, height=1, bg="blue", command = pokevisor_video_ui_start).pack()
    
    
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
