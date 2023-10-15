import tkinter as tk

import customtkinter
import customtkinter as ctk
from PIL import Image

from magic import Magic
from ConfigService import RotoConfig

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

theme_img = ctk.CTkImage(dark_image=Image.open("./assets/GFX/sun.png"), light_image=Image.open("./assets/GFX/moon.png"), size=(20, 20))

class Button(ctk.CTkButton):
    def __init__(self, master, fg_color='brown', hover_color="#721d1d", *args, **kwargs):
        super().__init__(master=master, fg_color=fg_color, hover_color=hover_color, corner_radius=4, *args, **kwargs)


class Label(ctk.CTkLabel):
    def __init__(self, master, text_color=("black", "white"), *args, **kwargs):
        super().__init__(master=master, font=ctk.CTkFont(family="helvetica", weight="bold", size=14), text_color=text_color, *args, **kwargs)


class RotoTabs(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.mode = None

        self.add("Startup").grid(pady=20)
        self.grid(row=0, column=0, sticky="nsew")

        # tab1 - Start up
        self.LblCurrentPath = Label(self.tab("Startup"), text="Current Path:")
        self.LblCurrentPath.grid(row=0, column=0, sticky="nsew")
        self.LblPath = Label(self.tab("Startup"), text=f"path.txt = {self.master.magic.path}")
        self.LblPath.grid(row=1, column=0, sticky="nsew")

        self.LblPathHelper = Label(self.tab("Startup"), text="Enter Client path below or Auto Detect when game is open")
        self.LblPathHelper.grid(row=2, column=0, sticky="", pady=(50, 0))

        self.EnterPathfield = ctk.CTkEntry(textvariable=self.master.pathfield, width=450, master=self.tab("Startup"), border_width=1,
                                           corner_radius=3)
        self.EnterPathfield.grid(row=3, column=0, sticky="")

        self.UpdatePathButton = Button(self.tab("Startup"), text='Update Path', command=self.master.magic.updatePath)
        self.AutoDetectPathButton = Button(self.tab("Startup"), text='Auto Detect Path', command=lambda: self.master.magic.updatePathField('PMU.exe'), fg_color='green', hover_color="#004d00")
        self.UpdatePathButton.grid(row=4, column=0, sticky="", pady=10)
        self.AutoDetectPathButton.grid(row=5, column=0, sticky="", pady=10)

        self.tab("Startup").columnconfigure(0, weight=1)
        self.tab("Startup").rowconfigure((0, 1, 2, 4, 5), weight=1)

        # tab 2 - GFX - deleted

        # tab 3 - SFX
        self.add("SFX Mods")

        # SFX Buttons
        self.SFXMuteButton = Button(self.tab("SFX Mods"), text='Enable Silent Client', command=self.master.magic.mute, fg_color='brown')
        self.SFXUnMuteButton = Button(self.tab("SFX Mods"), text='Disable Silent Client', command=self.master.magic.unmute,
                                      fg_color='brown')
        self.SFXMuteButton.grid(row=0, column=0)
        self.SFXUnMuteButton.grid(row=0, column=1, sticky="")

        self.SFXResetButton = Button(self.tab("SFX Mods"), text='Reset SFX Folders', command=self.master.magic.sfxResetFolder,
                                     fg_color='brown')
        self.SFXResetButton.grid(row=2, column=0, columnspan=2, sticky="", pady=(0, 10))

        # Current Mode Labels
        self.SFXLbl = Label(self.tab("SFX Mods"), text="Current Mode: ")
        self.SFXStatusLbl = Label(self.tab("SFX Mods"), text=self.master.magic.getSfxState(), text_color='orange red')
        self.SFXLbl.grid(row=1, column=0, columnspan=1, sticky="e")
        self.SFXStatusLbl.grid(row=1, column=1, columnspan=1, sticky="w")

        self.tab("SFX Mods").rowconfigure((0, 1), weight=1)
        self.tab("SFX Mods").columnconfigure((0, 1), weight=1)

        self.exitButton = Button(self, text='Exit', command=master.exit, fg_color='brown', width=100)
        self.exitButton.grid(row=5, sticky="s", pady=(10, 10))

        self.statusLbl = Label(self, text="status", text_color='green')
        self.statusLbl.grid(row=6, column=0, sticky="sw", ipadx=10)

        self.mode = customtkinter.get_appearance_mode()
        self.modebutton = Button(self, text="", image=theme_img, fg_color=None, hover_color=None, command=self.themechange, width=10)
        self.modebutton.grid(row=0, column=0, sticky="e")

    def themechange(self):
        if self.mode == "Dark":
            self.master.rotoconfig.setConfig('appearance','light')
            customtkinter.set_appearance_mode("light")
            self.mode = customtkinter.get_appearance_mode()
        else:
            self.master.rotoconfig.setConfig('appearance','dark')
            customtkinter.set_appearance_mode("dark")
            self.mode = customtkinter.get_appearance_mode()


class RotoView(ctk.CTk):
    def __init__(self):
        super().__init__()
        #Config for Rotoview
        self.rotoconfig = RotoConfig()
        self.magic = Magic(self)
        self.pathfield = tk.StringVar()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.tabber = RotoTabs(master=self, segmented_button_fg_color=None)
        self.tabber.grid(row=0, column=0, padx=20, pady=20)
        self.tabber._segmented_button.grid(sticky="w")

        # rotom logo
        img = ctk.CTkImage(Image.open("./assets/GFX/smol.png"), size=(77, 77))
        rotom = ctk.CTkLabel(self, image=img, text="")
        rotom.image = img
        rotom.place(relx=1.0, rely=1.0, anchor='s')
        # end of logo

        self.iconphoto(False, tk.PhotoImage(file="rotoview.png"))
        self.title('Rotoview-v0.3.2')

        self.geometry()
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height() - 50)
        customtkinter.set_appearance_mode(self.rotoconfig.getConfig('appearance'))

    def exit(self):
        self.destroy()
        self.quit()
