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

        #************** Main System ************************
class PhernSoftware(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("500x500")
        self.resizable(width=tkinter.FALSE , height=tkinter.FALSE)
        
        self.title_font = tkfont.Font(family='Helvetica', size=12, weight="bold", slant="italic")
        self.title("PhernSoftware")


        #********************Add Menu***********************
        menu= Menu(self)  
        self.config(menu = menu)
        subMenu= Menu(menu)
        menu.add_cascade(label = "Hakkinda",menu = subMenu)
        subMenu.add_command(label = "Versiyon",command= lambda: self.show_frame("UpdatePage"))
        subMenu.add_command(label = "Yetkili")
        
        #*************** Main Settings *********************
        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
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
        controller.geometry("400x500")

        #*********************** Sign Up ********************
        def receive():
            """Handles receiving of messages."""
            while True:
                try:
                    msg = client_socket.recv(BUFSIZ).decode("utf8")
                    msg_list.insert(tkinter.END, msg)
                except OSError:  # Possibly client has left the chat.
                    break
                
        def send(event=None):  # event is passed by binders.
            """Handles sending of messages."""
            msg = my_msg.get()
            my_msg.set("")  # Clears input field.
            client_socket.send(bytes(msg, "utf8"))
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
        entry_field.place(x=128, y=431, height=60, width=265)
        group_button = tkinter.Button(self, bg="#ffbf00", activebackground="#facc2e", text="Yeni Grup", font=30, command=lambda: controller.show_frame("NewRoom"))
        group_button.place(x=6, y=385, height=40, width=115)
        add_button = tkinter.Button(self, bg="#ffbf00", activebackground="#facc2e", text="Ekle", font=30)
        add_button.place(x=128, y=385, height=40, width=100)
        set_button = tkinter.Button(self, bg="#ffbf00", activebackground="#facc2e", text="Ayarlar", font=30)
        set_button.place(x=235, y=385, height=40, width=115)
        menu_button = tkinter.Button(self, bg="#ffbf00", activebackground="#facc2e", text="#", font=30)
        menu_button.place(x=356, y=385, height=40, width=40)
        send_button = tkinter.Button(self, bg="#ffbf00", activebackground="#facc2e", text="Gönder", font=30, command=send)
        send_button.place(x=6, y=431, height=60, width=115)

        receive_thread = Thread(target=receive)
        receive_thread.start()
        

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

    def __init__(self ,parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        def receive():
            """Handles receiving of messages."""
            while True:
                try:
                    msg = client_socket.recv(BUFSIZ).decode("utf8")
                    msg_list.insert(tkinter.END, msg)
                except OSError:  # Possibly client has left the chat.
                    break
                
        def send(event=None):  # event is passed by binders.
            """Handles sending of messages."""
            msg = my_msg.get()
            my_msg.set("")  # Clears input field.
            client_socket.send(bytes(msg, "utf8"))
            if msg == "{quit}":
                client_socket.close()
                self.quit()

        def on_closing(event=None):
            """This function is to be called when the window is closed."""
            my_msg.set("{quit}")
            send()
        
        my_msg = tkinter.StringVar()
        my_msg.set("")
        scrollbar = tkinter.Scrollbar(self)
        msg_list = tkinter.Listbox(self, bd=0, bg="white", font="Arial", height=20, width=50, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        msg_list.pack()


        entry_field = tkinter.Entry(self, textvariable=my_msg, font=30)
        entry_field.bind("<Return>", send)
        entry_field.place(x=128, y=431, height=60, width=265)
        group_button = tkinter.Button(self, bg="#ffbf00", activebackground="#facc2e", text="Yeni Grup", font=30, command=lambda: controller.show_frame("NewRoom"))
        group_button.place(x=6, y=385, height=40, width=115)
        add_button = tkinter.Button(self, bg="#ffbf00", activebackground="#facc2e", text="Ekle", font=30)
        add_button.place(x=128, y=385, height=40, width=100)
        set_button = tkinter.Button(self, bg="#ffbf00", activebackground="#facc2e", text="Ayarlar", font=30)
        set_button.place(x=235, y=385, height=40, width=115)
        menu_button = tkinter.Button(self, bg="#ffbf00", activebackground="#facc2e", text="#", font=30)
        menu_button.place(x=356, y=385, height=40, width=40)
        send_button = tkinter.Button(self, bg="#ffbf00", activebackground="#facc2e", text="Gönder", font=30, command=send)
        send_button.place(x=6, y=431, height=60, width=115)

        receive_thread = Thread(target=receive)
        receive_thread.start()

        

        
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

if __name__ == "__main__":
    app = PhernSoftware()
    app.mainloop()

