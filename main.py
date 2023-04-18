import traceback
import shutil
import webbrowser
# from magic import *
import tkinter as tk

class magic:
    def restore():
        shutil.copy("./Chara-479.chara","{0}/Chara-479.chara".format(path+"/Sprites"))
        shutil.copy("./Portrait-479.portrait","{0}/Portrait-479.portrait.".format(path+"/Mugshots"))
        label2.config(text="Restored Rotom")
    def replace(id):
        try:
            shutil.copy("{0}/Chara-{1}.chara".format(path+"/Sprites",id),"{0}/Chara-479.chara".format(path+"/Sprites"))
            shutil.copy("{0}/Portrait-{1}.portrait".format(path+"/Mugshots",id),"{0}/Portrait-479.portrait".format(path+"/Mugshots"))
            label2.config(text="Updated {0} to {1}".format("479",id))
        except IOError:
            label2.config(text="Err Invalid File")

try:
    with open('path.txt', 'r') as file:
        path = file.read().rstrip()
    root= tk.Tk()
except IOError:
    path = "path.txt not found"

try:
    canvas1 = tk.Canvas(root, width = 800, height = 500)
    root.title('Rotoview-v0.1.1')
    canvas1.pack()

    def exit():
        root.destroy()
        root.quit()
        
    
    def openpage():
       webbrowser.open("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_with_form_differences",new=2)
        
    def show():
        canvas1.create_window(50,300,window=tk.Label(root,text=path, fg='blue', font=('helvetica', 12, 'bold')))

    entry1 = tk.Entry(root)
    canvas1.create_window(330,50,window=entry1)

    label3 = tk.Label(root,text="Enter Dex Number", fg='blue', font=('helvetica', 12, 'bold'))
    canvas1.create_window(330,30,window=label3)

    #rotom logo
    img = tk.PhotoImage(file="smol.png")
    label4 = tk.Label(root, image=img)
    label4.place(relx=1.0, rely=1.0, anchor='s')
    #end of logo

    button1 = tk.Button(text='Replace', command=lambda:magic.replace(entry1.get()), bg='brown',fg='white')
    button2 = tk.Button(text='Restore', command=magic.restore, bg='brown',fg='white')
    button3 = tk.Button(text='Exit', command=exit, bg='brown',fg='white')
    button4 = tk.Button(text='Poke with Forms List', command=openpage, bg='brown',fg='white')

    canvas1.create_window(280, 100, window=button1)
    canvas1.create_window(380, 100, window=button2)
    canvas1.create_window(320, 150, window=button3)
    canvas1.create_window(320, 350, window=button4)

    label1 = tk.Label(root, text= "path.txt = "+path, fg='blue', font=('helvetica', 12, 'bold'))
    canvas1.create_window(350, 200, window=label1)

    label2 = tk.Label(root, text="status", fg='green', font=('helvetica', 12, 'bold'))
    canvas1.create_window(350, 250, window=label2)



    root.mainloop()
except Exception as e:
    with open('log.txt', 'a') as f:
        f.write(str(e))
        f.write(traceback.format_exc())
