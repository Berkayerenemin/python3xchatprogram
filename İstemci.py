import socket


host = "127.0.0.1"
port = 1221
buf = 1024
calistir = (host,port)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(calistir)

while True:
        gonder = input(">> ")
        s.sendall(gonder.encode('utf-8'))
        if gonder == "q":
                print ("Baglanti Kapatildi..")
                break


s.close()
