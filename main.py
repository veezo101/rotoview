import traceback
import shutil
import webbrowser
# from magic import *
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD

class magic:
    def restore():
        shutil.copy("./Chara-479.chara","{0}/Chara-479.chara".format(path+"/Sprites"))
        shutil.copy("./Portrait-479.portrait","{0}/Portrait-479.portrait.".format(path+"/Mugshots"))
        statusLabel.config(text="Restored Rotom")
    def replace(id):
        try:
            shutil.copy("{0}/Chara-{1}.chara".format(path+"/Sprites",id),"{0}/Chara-479.chara".format(path+"/Sprites"))
            shutil.copy("{0}/Portrait-{1}.portrait".format(path+"/Mugshots",id),"{0}/Portrait-479.portrait".format(path+"/Mugshots"))
            statusLabel.config(text="Updated {0} to {1}".format("479",id))
        except IOError:
            statusLabel.config(text="Err Invalid File")

try:
    with open('path.txt', 'r') as file:
        path = file.read().rstrip()
    root= tk.Tk()
    root.iconbitmap("rotoview.ico")
    root.title('Rotoview-v0.2.1')
    root.geometry("600x400")

    #staus label
    statusLabel = tk.Label(root, text="status", fg='green', font=('helvetica', 12, 'bold'))
    statusLabel.place(relx=0.0,rely=1.0,anchor='sw')

    #define exit
    def exit():
        root.destroy()
        root.quit()
    
    #exit button
    exitButton = tk.Button(text='Exit', command=exit, bg='brown',fg='white',width=10)
    exitButton.pack(side="bottom",pady=(5,30))

except IOError:
    path = "path.txt not found"

try:    
    
    def openpage():
       webbrowser.open("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_with_form_differences",new=2)
        
    # def show():
    #     canvas1.create_window(50,300,window=tk.Label(root,text=path, fg='blue', font=('helvetica', 12, 'bold')))

    #rotom logo
    img = tk.PhotoImage(file="smol.png")
    label4 = tk.Label(root, image=img)
    label4.place(relx=1.0, rely=1.0, anchor='s')
    #end of logo
    
    #Notebook Widget
    notebook = ttk.Notebook(root,width=600,height=430)
    notebook.pack(padx=20,pady=20)

    #tab1 - Start up
    tab1 = ttk.Frame(notebook)
    labelCurrentPath = tk.Label(tab1, text= "Current Path:", fg='blue', font=('helvetica', 12, 'bold')) 
    labelPath = tk.Label(tab1, text= "path.txt = "+path, fg='blue', font=('helvetica', 12, 'bold'))
    labelCurrentPath.pack()
    labelPath.pack()

    #tab 2 - GFX
    tab2 = ttk.Frame(notebook)
    
    ##Enter dex number
    EnterDexHelperLabel = tk.Label(tab2,text="Use Rotom in game to view the desired sprite", fg='blue', font=('helvetica', 12, 'bold'))
    EnterDexLabel = tk.Label(tab2,text="Enter Dex Number", fg='blue', font=('helvetica', 12, 'bold'))
    EnterDexHelperLabel.place(relx=0.5,rely=0.12,anchor="center")
    EnterDexLabel.place(relx=0.5,rely=0.25,anchor="center")
    EnterDexField = tk.Entry(tab2)
    EnterDexField.place(relx=0.5,rely=0.34,anchor="center")

    ##GFX Buttons
    GFXReplaceButton = tk.Button(tab2,text='Replace', command=lambda:magic.replace(EnterDexField.get()), bg='brown',fg='white')
    GFXRestoreButton = tk.Button(tab2,text='Restore', command=magic.restore, bg='brown',fg='white')
    GFXPokeListButton = tk.Button(tab2,text='Poke with Forms List', command=openpage, bg='mediumblue',fg='white')

    GFXReplaceButton.place(relx=0.44,rely=0.45,anchor="center")
    GFXRestoreButton.place(relx=0.56,rely=0.45,anchor="center")
    GFXPokeListButton.place(relx=0.5,rely=0.57,anchor="center")

    #tab 3 - SFX
    tab3 = ttk.Frame(notebook)

    
    notebook.add(tab1,text='Start up')
    notebook.add(tab2,text='GFX Mods')
    notebook.add(tab3,text='SFX Mods')

    root.mainloop()
except Exception as e:
    with open('log.txt', 'a') as f:
        f.write(str(e))
        f.write(traceback.format_exc())
