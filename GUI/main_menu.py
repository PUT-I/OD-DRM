import tkinter.ttk as ttk
from tkinter import Tk, messagebox, StringVar

from poke_visor.gui.chip_classifier_generator_ui import main as chip_main
from poke_visor.gui.pokevisor_image_ui import main as image_main
from poke_visor.gui.pokevisor_video_ui import main as video_main
from serial_key_generator import key_validator as kv


class KeyRegistrationUi(Tk):
    def __init__(self):
        super().__init__(None)
        self.geometry("300x150")
        self.title("PokeVisor key registration")

        ttk.Label(self, text="Please enter your serial key below").pack()

        self._key = StringVar()

        key_entry_frame = ttk.LabelFrame(self, text="Serial key")
        self._key_entry = ttk.Entry(key_entry_frame, width=40, textvariable=self._key)
        self._key_entry.pack(padx=5, pady=5)
        key_entry_frame.pack(padx=5, pady=5)

        ttk.Button(self, text="Register", width=10, command=self.validate).pack()

    def validate(self):
        if kv.check_key(self._key.get()) == kv.Key.GOOD:
            self.destroy()
            MainMenuUi()
        else:
            messagebox.showinfo("error", "Wrong key")
        return True


class MainMenuUi(Tk):
    def __init__(self):
        super().__init__(None)
        self.geometry("200x150")
        self.title("PokeVisor")

        # sets the geometry of toplevel
        ttk.Button(self,
                   text="Chip classifier generator",
                   width=30,
                   command=self.start_chip_classifier_generator).pack(padx=5, pady=5)

        ttk.Button(self,
                   text="PokeVisor image",
                   width=30,
                   command=self.start_pokevisor_ui).pack(padx=5, pady=5)

        ttk.Button(self,
                   text="PokeVisor video",
                   width=30,
                   command=self.start_pokevisor_video).pack(padx=5, pady=5)

    def start_pokevisor_ui(self):
        self.destroy()
        image_main()
        MainMenuUi()

    def start_chip_classifier_generator(self):
        self.destroy()
        chip_main()
        MainMenuUi()

    def start_pokevisor_video(self):
        self.destroy()
        video_main()
        MainMenuUi()


def main_account_screen():
    key_activation = KeyRegistrationUi()
    key_activation.mainloop()


if __name__ == "__main__":
    main_account_screen()
