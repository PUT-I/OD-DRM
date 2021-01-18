""" This script contains key validation and main menu ui classes. """

import tkinter.ttk as ttk
import winreg
from tkinter import Tk, messagebox, StringVar
from winreg import  KEY_ALL_ACCESS

from poke_visor.gui.chip_classifier_generator_ui import main as chip_main
from poke_visor.gui.pokevisor_image_ui import main as image_main
from poke_visor.gui.pokevisor_video_ui import main as video_main
from serial_key_generator.key_validator import KeyValidator, KeyStatus


class KeyValidationUi(Tk):
    """ This class represents key validation window. """

    def __init__(self):
        """ Initializes KeyValidationUi class. """

        super().__init__(None)

        self._key = StringVar()
        """ Stores product key entered by user. """

        self.geometry("300x150")
        self.title("PokeVisor key registration")

        ttk.Label(self, text="Please enter your serial key below").pack()
        key_entry_frame = ttk.LabelFrame(self, text="Serial key")
        ttk.Entry(key_entry_frame, width=40, textvariable=self._key).pack(padx=5, pady=5)
        key_entry_frame.pack(padx=5, pady=5)

        ttk.Button(self, text="Register", width=10, command=self._validate).pack()

    def _validate(self) -> None:
        """ Handles user entered key validation. """
        key_written=self._key.get()
        if KeyValidator.check_key(key_written) == KeyStatus.VALID:
            self.destroy()
            access_registry = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
            access_key = winreg.OpenKey(access_registry,r"SOFTWARE")
            key=winreg.CreateKey(access_registry,"SOFTWARE\Pokevisor")
            winreg.SetValueEx(key, "key", 0, winreg.REG_SZ,key_written)
            winreg.CloseKey(key)
            MainMenuUi()
        else:
            messagebox.showinfo("error", "Wrong key")


class MainMenuUi(Tk):
    """ This class represents main menu window. """

    def __init__(self):
        """ Initializes MainMenuUi class. """

        super().__init__(None)
        self.geometry("200x150")
        self.title("PokeVisor")

        # sets the geometry of toplevel
        ttk.Button(self,
                   text="Chip classifier generator",
                   width=30,
                   command=self._start_chip_classifier_generator).pack(padx=5, pady=5)

        ttk.Button(self,
                   text="PokeVisor image",
                   width=30,
                   command=self._start_pokevisor_image).pack(padx=5, pady=5)

        ttk.Button(self,
                   text="PokeVisor video",
                   width=30,
                   command=self._start_pokevisor_video).pack(padx=5, pady=5)

    def _start_chip_classifier_generator(self) -> None:
        """ Starts chip classifier generator. After closing generator window main menu will open again. """

        self.destroy()
        chip_main()
        MainMenuUi()

    def _start_pokevisor_image(self) -> None:
        """ Starts PokeVisor in image mode. After closing PokeVisor window main menu will open again. """

        self.destroy()
        image_main()
        MainMenuUi()

    def _start_pokevisor_video(self) -> None:
        """ Starts PokeVisor in video mode. After closing PokeVisor window main menu will open again. """

        self.destroy()
        video_main()
        MainMenuUi()


def _main() -> None:
    """ Main function """
    access_registry = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
    try:
        #checks for key in registry
       
        key = winreg.OpenKey(access_registry, r"SOFTWARE\Pokevisor")
        key_from_registry=winreg.QueryValueEx(key, "key")[0]
        winreg.CloseKey(key)
        if KeyValidator.check_key(key_from_registry) == KeyStatus.VALID:
            MainMenuUi().mainloop()
        else:
            key_activation = KeyValidationUi()
            key_activation.mainloop()


    except:
        key_activation = KeyValidationUi()
        key_activation.mainloop()


if __name__ == "__main__":
    _main()
