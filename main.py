import traceback
import shutil
import webbrowser
# from magic import *
import tkinter as tk
from tkinter import ttk
import os
import zipfile
import psutil
from tkinterdnd2 import DND_FILES, TkinterDnD

class magic:
    def updatePathField(process_name):
        try:
            for process in psutil.process_iter(['pid', 'name']):
                if process.info['name'] == process_name:
                        process_exe_path = psutil.Process(process.info['pid']).exe()
                        pathfield.set(str(process_exe_path.rpartition('\\')[0]))
                        statusLabel.config(text="Successfully detected path")
                        return
            statusLabel.config(text="Failed to auto detect path. Make sure the client is open!")        
        except Exception as ex:
            pathfield.set('')
    
    def updatePath():
        try:
            file = open("path.txt","w")
            file.write(pathfield.get())
            file.close()
            statusLabel.config(text='Successfully updated path')

            writtenFile = open('path.txt', 'r')
            global path
            path = writtenFile.read().rstrip()
            labelPath.config(text="path.txt="+path)
            statusLabel.config(text='Successfully updated and read path')
        except Exception as ex:
            statusLabel.config(text="Error: {0} args: {1}".format(type(ex).__name__,ex.args))
    
    def sfxGetCurrentState():
        if(os.path.exists('{0}/PMU.exe'.format(path))==False):
            return "invalidpath"
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
            currentState = magic.sfxGetCurrentState()
            if(currentState=="invalidpath"):
                statusLabel.config(text="Invalid Game Path!")
                SFXCurrentModeStatusLabel.config(text=magic.sfxGetCurrentState())
                return
            if(currentState=="muted"):
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
            if(currentState=="invalidpath"):
                statusLabel.config(text="Invalid Game Path!")
                SFXCurrentModeStatusLabel.config(text=magic.sfxGetCurrentState())
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
            if(currentState=="invalidpath"):
                statusLabel.config(text="Invalid Game Path!")
                SFXCurrentModeStatusLabel.config(text=magic.sfxGetCurrentState())
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
    root.title('Rotoview-v0.2.5')
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
    labelCurrentPath = tk.Label(tab1, text= "Current Path:", fg='blue', font=('helvetica', 12, 'bold'),pady=1) 
    labelPath = tk.Label(tab1, text= "path.txt = "+path, fg='blue', font=('helvetica', 12, 'bold'),pady=1)
    labelCurrentPath.pack()
    labelPath.pack()

    labelPathHelper = tk.Label(tab1, text= "Enter Client path or Auto Detect when game is open", fg='blue', font=('helvetica', 12, 'bold'),pady=1)
    labelPathHelper.place(relx=0.5,rely=0.4,anchor="center")

    pathfield = tk.StringVar()
    EnterPathfield = tk.Entry(tab1,textvariable=pathfield,width=80)
    EnterPathfield.place(relx=0.5,rely=0.5,anchor="center")

    UpdatePathButton = tk.Button(tab1,text='Update Path', command=magic.updatePath, bg='brown',fg='white')
    AutoDetectPathButton = tk.Button(tab1,text='Auto Detect Path', command=lambda:magic.updatePathField('PMU.exe'), bg='green',fg='white')
    UpdatePathButton.place(relx=0.5,rely=0.65,anchor="center")
    AutoDetectPathButton.place(relx=0.5,rely=0.8,anchor="center")

    #tab 2 - GFX - deleted

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
    notebook.add(tab3,text='SFX Mods')

    root.mainloop()
except Exception as e:
    with open('log.txt', 'a') as f:
        f.write(str(e))
        f.write(traceback.format_exc())
