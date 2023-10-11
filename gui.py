import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from magic import Magic


# Defined a tk.Label subclass, so you don't have to put the same font every single time you add a label
class Label(tk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(font=('helvetica', 12, 'bold'), *args, **kwargs)

class RotoView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.tabs = {}
        self.magic = Magic(self)
        self.grid()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # rotom logo
        img = ImageTk.PhotoImage(Image.open("./assets/GFX/smol.png"))
        rotom = tk.Label(self, image=img)
        rotom.image = img
        rotom.place(relx=1.0, rely=1.0, anchor='s')
        # end of logo

        self.iconbitmap("rotoview.ico")
        self.title('Rotoview-v0.2.5')

        # Notebook Widget
        notebook = ttk.Notebook(self, width=550, height=300)
        notebook.grid(padx=20, pady=20)

        # tab1 - Start up
        self.tab_startup = ttk.Frame(notebook, padding=20)
        self.LblCurrentPath = Label(self.tab_startup, text="Current Path:", fg='blue')
        self.LblCurrentPath.grid(row=0, column=0, sticky="")
        self.LblPath = Label(self.tab_startup, text=f"path.txt = {self.magic.path}", fg='blue')
        self.LblPath.grid(row=1, column=0, sticky="")

        self.LblPathHelper = Label(self.tab_startup, text="Enter Client path below or Auto Detect when game is open", fg='blue')
        self.LblPathHelper.grid(row=2, column=0, sticky="", pady=(50, 0))

        self.pathfield = tk.StringVar()
        self.EnterPathfield = tk.Entry(self.tab_startup, textvariable=self.pathfield, width=75)
        self.EnterPathfield.grid(row=3, column=0, sticky="")

        self.UpdatePathButton = tk.Button(self.tab_startup, text='Update Path', command=self.magic.updatePath, bg='brown', fg='white')
        self.AutoDetectPathButton = tk.Button(self.tab_startup, text='Auto Detect Path', command=lambda: self.magic.updatePathField('PMU.exe'), bg='green', fg='white')
        self.UpdatePathButton.grid(row=4, column=0, sticky="", pady=10)
        self.AutoDetectPathButton.grid(row=5, column=0, sticky="", pady=10)

        for i, _ in enumerate(self.tab_startup.children):
            self.tab_startup.columnconfigure(i, weight=1)
            if i not in (1, 0):
                self.tab_startup.rowconfigure(i, weight=1)

        self.tabs["Start up"] = self.tab_startup

        # tab 2 - GFX - deleted

        # tab 3 - SFX
        self.tab_sfx = ttk.Frame(notebook, padding=100)

        # SFX Buttons
        self.SFXMuteButton = tk.Button(self.tab_sfx, text='Enable Silent Client', command=self.magic.mute, bg='brown', fg='white', takefocus=False)
        self.SFXUnMuteButton = tk.Button(self.tab_sfx, text='Disable Silent Client', command=self.magic.unmute, bg='brown', fg='white', takefocus=False)
        self.SFXMuteButton.grid(row=0, column=0,  sticky="")
        self.SFXUnMuteButton.grid(row=0, column=1,  sticky="")

        self.SFXResetButton = tk.Button(self.tab_sfx, text='Reset SFX Folders', command=self.magic.sfxResetFolder, bg='brown', fg='white', takefocus=False)
        self.SFXResetButton.grid(row=2, column=0, columnspan=2, sticky="")

        # Current Mode Labels
        self.SFXLbl = Label(self.tab_sfx, text="Current Mode: ", fg='blue')
        self.SFXStatusLbl = Label(self.tab_sfx, text=self.magic.getSfxState(), fg='orange red')
        self.SFXLbl.grid(row=1, column=0, columnspan=1, sticky="e", pady=20)
        self.SFXStatusLbl.grid(row=1, column=1, columnspan=1, sticky="", pady=20, padx=(0, 50))

        self.tab_sfx.columnconfigure(0, weight=1)
        self.tab_sfx.columnconfigure(1, weight=1)

        self.tabs["SFX Mods"] = self.tab_sfx

        [notebook.add(tab, text=k) for k, tab in self.tabs.items()]

        self.exitButton = tk.Button(text='Exit', command=exit, bg='brown', fg='white', width=10)
        self.exitButton.grid(row=5, sticky="s")

        self.statusLbl = Label(self, text="status", fg='green')
        self.statusLbl.grid(row=6, column=0, sticky="sw")

    def exit(self):
        self.destroy()
        self.quit()
