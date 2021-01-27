""" This script contains key validation and main menu ui classes. """
import base64
import hashlib
import json
import tkinter.ttk as ttk
from enum import Enum
from http.client import HTTPConnection
from tkinter import Tk, messagebox, StringVar

from poke_visor.gui.chip_classifier_generator_ui import main as chip_main
from poke_visor.gui.pokevisor_image_ui import main as image_main
from poke_visor.gui.pokevisor_video_ui import main as video_main
from serial_key_generator.key_validator import KeyValidator, KeyStatus


class AuthorizationType(Enum):
    serial_key = "serialKey"
    server = "server"


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

        if KeyValidator.check_key(self._key.get()) == KeyStatus.VALID:
            self.destroy()
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


class LoginUi(Tk):
    """ This class represents key login window. """

    def __init__(self):
        """ Initializes LoginUi class. """

        super().__init__(None)

        self._username = StringVar()
        self._password = StringVar()
        """ Stores product key entered by user. """

        self.geometry("300x200")
        self.title("PokeVisor login")

        ttk.Label(self, text="Enter user credentials").pack()
        username_frame = ttk.LabelFrame(self, text="Username")
        ttk.Entry(username_frame, width=40, textvariable=self._username).pack(padx=5, pady=5)
        username_frame.pack(padx=5, pady=5)
        password_frame = ttk.LabelFrame(self, text="Password")
        ttk.Entry(password_frame, show="*", width=40, textvariable=self._password).pack(padx=5, pady=5)
        password_frame.pack(padx=5, pady=5)

        ttk.Button(self, text="Login", width=10, command=self._login).pack()
        ttk.Button(self, text="Register", width=10, command=self._go_to_register).pack()

    def _go_to_register(self) -> None:
        """ Handles user entered key validation. """

        self.destroy()
        RegisterUi()

    def _login(self) -> None:
        """ Handles user entered key validation. """

        error_msg = ""
        if not self._username.get().strip():
            error_msg += "Empty username\n"

        if not self._password.get().strip():
            error_msg += "Empty password\n"

        if error_msg:
            messagebox.showinfo("error", error_msg)
            return

        try:
            conn = HTTPConnection("localhost:5000")
            headers = {"Content-type": "application/json"}
            conn.request("POST", url="/user/authorize", headers=headers, body=json.dumps({
                "username": self._username.get(),
                "password": self._password.get()
            }))
            response = conn.getresponse()
            conn.close()
        except:
            messagebox.showinfo("error", "Could not connect to server")
            return

        if response.status == 200:
            self.destroy()
            MainMenuUi()
        else:
            messagebox.showinfo("error", "Login failed")


class RegisterUi(Tk):
    """ This class represents key login window. """

    def __init__(self):
        """ Initializes LoginUi class. """

        super().__init__(None)

        self._username = StringVar()
        self._password = StringVar()
        """ Stores product key entered by user. """

        self.geometry("300x200")
        self.title("PokeVisor registration")

        ttk.Label(self, text="Enter user credentials").pack()
        username_frame = ttk.LabelFrame(self, text="Username")
        ttk.Entry(username_frame, width=40, textvariable=self._username).pack(padx=5, pady=5)
        username_frame.pack(padx=5, pady=5)
        password_frame = ttk.LabelFrame(self, text="Password")
        ttk.Entry(password_frame, show="*", width=40, textvariable=self._password).pack(padx=5, pady=5)
        password_frame.pack(padx=5, pady=5)

        ttk.Button(self, text="Register", width=10, command=self._register_user).pack()
        ttk.Button(self, text="Cancel", width=10, command=self._go_back).pack()

    def _go_back(self) -> None:
        """ Handles user entered key validation. """

        self.destroy()
        LoginUi()

    def _register_user(self) -> None:
        """ Handles user entered key validation. """

        error_msg = ""
        if not self._username.get().strip():
            error_msg += "Empty username\n"

        if not self._password.get().strip():
            error_msg += "Empty password\n"

        if error_msg:
            messagebox.showinfo("error", error_msg)
            return

        try:
            conn = HTTPConnection("localhost:5000")
            headers = {"Content-type": "application/json"}
            password_hash: bytes = hashlib.sha256(self._password.get().encode("ascii")).digest()

            password: str = base64.b64encode(password_hash).decode(encoding="ascii")
            # password = password[:-1]

            conn.request("POST", url="/user", headers=headers, body=json.dumps({
                "username": self._username.get(),
                "password": password
            }))
            response = conn.getresponse()
            conn.close()
        except:
            messagebox.showinfo("error", "Could not connect to server")
            raise

        if response.status == 200:
            messagebox.showinfo("success", "User created")
            self._go_back()
        elif response.status == 409:
            messagebox.showinfo("error", "Username is already in use")
        else:
            messagebox.showinfo("error", "Server error")


def _main() -> None:
    """ Main function """

    with open("config.json", mode="r") as config_file:
        config: dict = json.loads(config_file.read())

    authorization_type = AuthorizationType(config["authorizationType"])
    if authorization_type == AuthorizationType.server:
        key_activation = LoginUi()
        key_activation.mainloop()
    elif authorization_type == AuthorizationType.serial_key:
        key_activation = KeyValidationUi()
        key_activation.mainloop()


if __name__ == "__main__":
    _main()
