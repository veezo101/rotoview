import traceback
import shutil
import webbrowser
# from magic import *
import tkinter as tk
from tkinter import ttk
import os
import zipfile
from tkinterdnd2 import DND_FILES, TkinterDnD

class magic:
    def restore():
        shutil.copy("./assets/GFX/Chara-479.chara","{0}/Chara-479.chara".format(path+"/GFX/Sprites"))
        shutil.copy("./assets/GFX/Portrait-479.portrait","{0}/Portrait-479.portrait.".format(path+"/GFX/Mugshots"))
        statusLabel.config(text="Restored Rotom. Relog to view changes")
    def replace(id):
        try:
            shutil.copy("{0}/Chara-{1}.chara".format(path+"/GFX/Sprites",id),"{0}/Chara-479.chara".format(path+"/GFX/Sprites"))
            shutil.copy("{0}/Portrait-{1}.portrait".format(path+"/GFX/Mugshots",id),"{0}/Portrait-479.portrait".format(path+"/GFX/Mugshots"))
            statusLabel.config(text="Updated {0} to {1}. Relog to view changes".format("479",id))
        except IOError:
            statusLabel.config(text="Err Invalid File")
    
    def sfxGetCurrentState():
        isExistSFX = os.path.exists('{0}/SFX'.format(path))
        isExistsRotoOG = os.path.exists('{0}/SFX-RotoOG'.format(path))
        isExistsRotoSilent = os.path.exists('{0}/SFX-RotoSilent'.format(path))
        if(isExistSFX == True and isExistsRotoSilent == False and isExistsRotoOG==True):
            return "muted"
        elif(isExistSFX == True and isExistsRotoSilent == False and isExistsRotoOG==False):
            return "clean"
        elif(isExistSFX == True and isExistsRotoSilent == True and isExistsRotoOG==False):
            return "unmuted"
        elif(isExistSFX==True and  isExistsRotoSilent == True and isExistsRotoOG==True):
            return "schrodinger"
        elif(isExistSFX==False and isExistsRotoOG==True):
            return "nosfxbutog"
        else:
            return "raiseResetFlag"
    
    def sfxResetFolder():
        try:
            if(magic.sfxGetCurrentState()=="muted"):
                os.rename("{0}/SFX".format(path),"{0}/SFX-RotoSilent".format(path))
            if(os.path.exists('{0}/SFX-RotoSilent'.format(path))):
                shutil.rmtree('{0}/SFX-RotoSilent'.format(path),ignore_errors=True)
            if(os.path.exists('{0}/SFX-RotoOG'.format(path))):
                if(os.path.exists('{0}/SFX'.format(path))):
                    shutil.rmtree('{0}/SFX'.format(path),ignore_errors=True)
                os.rename("{0}/SFX-RotoOG".format(path),"{0}/SFX".format(path))
            else:
                if(os.path.exists('{0}/SFX'.format(path))==False):
                    os.mkdir('{0}/SFX'.format(path))
            statusLabel.config(text="Successfully Restored SFX directory structure")
            SFXCurrentModeStatusLabel.config(text=magic.sfxGetCurrentState())
        except Exception as ex:
            if(type(ex)==PermissionError):
                statusLabel.config(text="Permission Error. Close the game client and retry.")
                SFXCurrentModeStatusLabel.config(text=magic.sfxGetCurrentState())
                return
            statusLabel.config(text="Error: {0} args: {1}".format(type(ex).__name__,ex.args))
            SFXCurrentModeStatusLabel.config(text=magic.sfxGetCurrentState())

    def mutePmu():
        try:
            currentState = magic.sfxGetCurrentState()
            if(currentState=="muted"):
                statusLabel.config(text="Already muted!")
                SFXCurrentModeStatusLabel.config(text=magic.sfxGetCurrentState())
                return
            
            if(currentState == "raiseResetFlag" or currentState=="schrodinger" or currentState=="nosfxbutog"):
                magic.sfxResetFolder()
                statusLabel.config(text="Folders Reset due to an error. Please try again")

            if(currentState=="clean"):
                with zipfile.ZipFile('./SilentSFX.zip','r') as silent_zip:
                    silent_zip.extractall('{0}/SFX-RotoSilent'.format(path))
                os.rename("{0}/SFX".format(path),"{0}/SFX-RotoOG".format(path))
                os.rename("{0}/SFX-RotoSilent".format(path),"{0}/SFX".format(path))
                statusLabel.config(text="Client successfully muted except shiny")
                if(os.path.exists('./assets/SFX/magic838.ogg')):
                    shutil.copy('./assets/SFX/magic838.ogg',"{0}/SFX/magic838.ogg".format(path))
                statusLabel.config(text="Client successfully muted except custom shiny!")


            if(currentState=="unmuted"):
                os.rename("{0}/SFX".format(path),"{0}/SFX-RotoOG".format(path))
                statusLabel.config(text="Moved current to OG")
                os.rename("{0}/SFX-RotoSilent".format(path),"{0}/SFX".format(path))
                statusLabel.config(text="Client successfully muted except shiny")
                if(os.path.exists('./assets/SFX/magic838.ogg')):
                    shutil.copy('./assets/SFX/magic838.ogg',"{0}/SFX/magic838.ogg".format(path))
                    statusLabel.config(text="Client successfully muted except custom shiny!")

            SFXCurrentModeStatusLabel.config(text=magic.sfxGetCurrentState())

        except FileNotFoundError as ex:
            # statusLabel.config(text="Failed to find folders (SFX-RotoOG or SFX-RotoSilent)")
            statusLabel.config(text="Error: {0} args: {1}".format(type(ex).__name__,ex.args))
            SFXCurrentModeStatusLabel.config(text=magic.sfxGetCurrentState())
        except Exception as ex:
            statusLabel.config(text="Failed to mute client. Try again after closing the Client")
            SFXCurrentModeStatusLabel.config(text=magic.sfxGetCurrentState())
            #debug
            #statusLabel.config(text="Error: {0} args: {1}".format(type(ex).__name__,ex.args))

    def unMutePmu():
        try:
            currentState = magic.sfxGetCurrentState()
            if(currentState=="unmuted"):
                statusLabel.config(text="Already unmuted!")
                return
            
            if(currentState == "raiseResetFlag" or currentState=="schrodinger" or currentState=="nosfxbutog"):
                magic.sfxResetFolder()
                statusLabel.config(text="Folders Reset due to an error. Please try again")

            if(currentState=="clean"):
                with zipfile.ZipFile('./SilentSFX.zip','r') as silent_zip:
                    silent_zip.extractall('{0}/SFX-RotoSilent'.format(path))
                statusLabel.config(text="Client successfully unmuted")

            if(currentState=="muted"):
                os.rename("{0}/SFX".format(path),"{0}/SFX-RotoSilent".format(path))
                os.rename("{0}/SFX-RotoOG".format(path),"{0}/SFX".format(path))
                statusLabel.config(text="Client successfully unmuted")

            SFXCurrentModeStatusLabel.config(text=magic.sfxGetCurrentState())

        except FileNotFoundError as ex:
            # statusLabel.config(text="Failed to find folders (SFX-RotoOG or SFX-RotoSilent)")
            statusLabel.config(text="Error: {0} args: {1}".format(type(ex).__name__,ex.args))
            SFXCurrentModeStatusLabel.config(text=magic.sfxGetCurrentState())
        except Exception as ex:
            statusLabel.config(text="Failed to mute client. Try again after closing the Client")
            SFXCurrentModeStatusLabel.config(text=magic.sfxGetCurrentState())
            #debug
            #statusLabel.config(text="Error: {0} args: {1}".format(type(ex).__name__,ex.args))
        


try:
    with open('path.txt', 'r') as file:
        path = file.read().rstrip()
    root= tk.Tk()
    root.iconbitmap("rotoview.ico")
    root.title('Rotoview-v0.2.3')
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
    img = tk.PhotoImage(file="./assets/GFX/smol.png")
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

    ##SFX Buttons
    SFXMuteButton = tk.Button(tab3,text='Enable Silent Client', command=magic.mutePmu, bg='brown',fg='white',takefocus=False)
    SFXUnMuteButton = tk.Button(tab3,text='Disable Silent Client', command=magic.unMutePmu, bg='brown',fg='white',takefocus=False)
    SFXResetButton = tk.Button(tab3,text='Reset SFX Folders', command=magic.sfxResetFolder, bg='brown',fg='white',takefocus=False)

    SFXMuteButton.place(relx=0.39,rely=0.45,anchor="center")
    SFXUnMuteButton.place(relx=0.61,rely=0.45,anchor="center")
    SFXResetButton.place(relx=0.50,rely=0.82,anchor="center")

    ##Current Mode Labels
    SFXCurrentModeLabel = tk.Label(tab3,text="Current Mode: ", fg='blue', font=('helvetica', 12, 'bold'))
    SFXCurrentModeStatusLabel = tk.Label(tab3,text=magic.sfxGetCurrentState(), fg='orange red', font=('helvetica', 12, 'bold'))
    SFXCurrentModeLabel.place(relx=0.39,rely=0.65,anchor="center")
    SFXCurrentModeStatusLabel.place(relx=0.55,rely=0.65,anchor="center")

    
    notebook.add(tab1,text='Start up')
    notebook.add(tab2,text='GFX Mods')
    notebook.add(tab3,text='SFX Mods')

    root.mainloop()
except Exception as e:
    with open('log.txt', 'a') as f:
        f.write(str(e))
        f.write(traceback.format_exc())
