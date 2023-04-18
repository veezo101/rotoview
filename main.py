import traceback
from magic import *
import tkinter as tk

try:

    with open('data.txt', 'r') as file:
        path = file.read().rstrip()
    root= tk.Tk()

    canvas1 = tk.Canvas(root, width = 300, height = 300)
    root.title('Rotoview')
    canvas1.pack()

    def hello ():  
        label1 = tk.Label(root, text= 'Hello World!', fg='blue', font=('helvetica', 12, 'bold'))
        canvas1.create_window(150, 200, window=label1)

    def exit():
        root.destroy()
        root.quit()
    
    def updatepath():
        path=entry1.get()
        
    def show():
        canvas1.create_window(50,300,window=tk.Label(root,text=path, fg='blue', font=('helvetica', 12, 'bold')))
        
    button1 = tk.Button(text='Replace', command=magic.replace, bg='brown',fg='white')
    button1 = tk.Button(text='ShowPath', command=show, bg='brown',fg='white')
    button2 = tk.Button(text='Restore', command=magic.restore, bg='brown',fg='white')
    button3 = tk.Button(text='Exit', command=exit, bg='brown',fg='white')
    button4 = tk.Button(text='Update Path', command=updatepath, bg='brown',fg='white')
    canvas1.create_window(30, 100, window=button1)
    canvas1.create_window(130, 100, window=button2)
    canvas1.create_window(80, 150, window=button3)
    canvas1.create_window(30, 5, window=button4)

    label1 = tk.Label(root, text= 'Enter path', fg='blue', font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 200, window=label1)

    entry1 = tk.Entry(root)
    canvas1.create_window(30,50,window=entry1)

    root.mainloop()
except Exception as e:
    with open('log.txt', 'a') as f:
        f.write(str(e))
        f.write(traceback.format_exc())
