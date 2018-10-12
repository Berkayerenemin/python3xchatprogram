from tkinter import messagebox as ms
import random                                  # python 3
from tkinter import *                          # python 3
import tkinter as tk                           # python 3
from tkinter import font  as tkfont            # python 3
from tkinter.filedialog import askopenfilename # python 3
from tkinter import messagebox                 # python 3
from math import *                             # python 3
#import Tkinter as tk                          # python 2
#import tkFont as tkfont                       # python 2
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import sqlite3

HOST = input('Host girin: ')
PORT = input('Port girin: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

with sqlite3.connect('quit.db') as db:
    c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL ,password TEX NOT NULL);')
    db.commit()

        #************** Main System ************************
class PhernSoftware(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=12, weight="bold", slant="italic")
        self.title("PhernSoftware")


        #********************Add Menu***********************
        menu= Menu(self)  
        self.config(menu = menu)
        subMenu= Menu(menu)
        menu.add_cascade(label = "Hakkinda",menu = subMenu)
        subMenu.add_command(label = "Versiyon",command= lambda: self.show_frame("UpdatePage"))
        subMenu.add_command(label = "Yetkili")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, NewRoom):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        
        #************ Pages *********************************

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.geometry("400x200")

        username = StringVar()
        password = StringVar()
        n_username = StringVar()
        n_password = StringVar()
        
        def login():
            with sqlite3.connect('quit.db') as db:
                c = db.cursor()
            find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
            c.execute(find_user, [(username.get()), (password.get())])
            result = c.fetchall()
            if result:
                logf.pack_forget()
                user = username.get()
                client_socket.send(user.encode("ascii"))
                controller.show_frame("NewRoom")
            else:
                ms.showerror('Oops!', 'Böyle bir kullanici bulunamadi.')

        def new_user():
            with sqlite3.connect('quit.db') as db:
                c = db.cursor()
            find_user = ("SELECT * FROM user WHERE username = ?")
            c.execute(find_user, [(username.get())])
            if c.fetchall():
                ms.showerror('Hata!', 'Bu kullanici adi kullanilmakta. Baska birini deneyin.')
            else:
                ms.showinfo("Harika!", "Hesabiniz basariyla açildi.")
                log()
            insert = 'INSERT INTO user(username,password) VALUES(?,?)'
            c.execute(insert, [(n_username.get()), (n_password.get())])
            db.commit()

        def log():
            username.set("")
            password.set("")
            crf.pack_forget()
            logf.pack()

        def cr():
            n_username.set("")
            n_password.set("")
            logf.pack_forget()
            crf.pack()

        logf = tk.Frame(self)
        label_0 = tk.Label(logf, text="Sistem Giris Formu", width=20, font="Times 18")
        label_0.pack()
        
        label_1 = tk.Label(logf, text="Kullanici Adi", width=20, font="Times 13")
        label_1.pack()

        entry_1 = tk.Entry(logf, textvariable=username)
        entry_1.pack()

        label_2 = tk.Label(logf, text="Sifre",width=20 ,font="Times 13")
        label_2.pack()

        entry_2 = tk.Entry(logf, textvariable=password)
        entry_2.pack()

        label_7 = tk.Label(logf, text="")
        label_7.pack()

        button1 = tk.Button(logf, text='Giris Yap', width=20, bg='brown', fg='white', font=("bold"),
                            command=login).pack()
        button3 = tk.Button(logf, text='Hesap Aç', width=20, bg='brown', fg='white', font=("bold"),
                            command=cr).pack()

        logf.pack()

        crf = tk.Frame(self)
        label_3 = tk.Label(crf, text="Sistem Giris Formu", width=20, font="Times 18")
        label_3.pack()

        label_4 = tk.Label(crf, text="Kullanici Adi", width=20, font="Times 13")
        label_4.pack()

        entry_3 = tk.Entry(crf, textvariable= n_username)
        entry_3.pack()

        label_5 = tk.Label(crf, text="Sifre", width=20, font="Times 13")
        label_5.pack()

        entry_4 = tk.Entry(crf, textvariable= n_password)
        entry_4.pack()

        label_6 = tk.Label(crf, text="")
        label_6.pack()
        
        button4 = tk.Button(crf, text='Kayit Ol', width=20, bg='brown', fg='white', font=("bold"),
                            command=new_user).pack()
        button5 = tk.Button(crf, text='Oturum Aç', width=20, bg='brown', fg='white', font=("bold"),
                            command=log).pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self,text="Ücretsiz Özellikler",width=20,font=("bold", 15))
        label.pack(side="top", fill="x", pady=10)
        button2 = tk.Button(self, text='Ekran Uygulamalari',width=20,bg='brown',fg='white',font=("bold"),
                            command=lambda: controller.show_frame("PageThree"))
        button3 = tk.Button(self, text='Hesap Makinesi',width=20,bg='brown',fg='white',font=("bold"),
                            command=lambda: controller.show_frame("EndPage"))
        button5 = tk.Button(self, text='Çikis Yap', width=20,bg='brown',fg='white',font=("bold"),
                            command=lambda: controller.show_frame("StartPage"))
        
        button2.pack()
        button3.pack()
        button5.pack()

class NewRoom(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.geometry("355x500")

        #*********************** Sign Up ********************
        def receive():
            """Handles receiving of messages."""
            while True:
                try:
                    msg = client_socket.recv(BUFSIZ).decode("ascii")
                    msg_list.insert(tkinter.END, msg)
                except OSError:  # Possibly client has left the chat.
                    break
                
        def send(event=None):  # event is passed by binders.
            """Handles sending of messages."""
            msg = my_msg.get()
            my_msg.set("")  # Clears input field.
            client_socket.send(msg.encode("ascii"))
            if msg == "{quit}":
                client_socket.close()
                self.quit()

        def on_closing(event=None):
            """This function is to be called when the window is closed."""
            my_msg.set("{quit}")
            send()


        #********************* Start Page Design ************
            

        my_msg = tkinter.StringVar()
        my_msg.set("")
        scrollbar = tkinter.Scrollbar(self)
        msg_list = tkinter.Listbox(self, bd=0, bg="white", font="Arial", height=20, width=50, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        msg_list.pack()


        entry_field = tkinter.Entry(self, textvariable=my_msg, font=30)
        entry_field.bind("<Return>", send)
        entry_field.place(x=128, y=431, height=60, width=210)
        group_button = tkinter.Button(self, bg="#ffbf00", activebackground="#facc2e", text="Yeni Grup", font=30, command=lambda: controller.show_frame("NewRoom"))
        group_button.place(x=6, y=385, height=40, width=115)
        add_button = tkinter.Button(self, bg="#ffbf00", activebackground="#facc2e", text="Ekle", font=30)
        add_button.place(x=128, y=385, height=40, width=100)
        set_button = tkinter.Button(self, bg="#ffbf00", activebackground="#facc2e", text="Geri Dön", font=30, command=lambda: controller.show_frame("StartPage"))
        set_button.place(x=235, y=385, height=40, width=115)
        send_button = tkinter.Button(self, bg="#ffbf00", activebackground="#facc2e", text="Gönder", font=30, command=send)
        send_button.place(x=6, y=431, height=60, width=115)

        receive_thread = Thread(target=receive)
        receive_thread.start()

if __name__ == "__main__":
    app = PhernSoftware()
    app.mainloop()
