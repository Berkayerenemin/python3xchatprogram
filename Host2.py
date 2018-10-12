import socket #İletişim için gereken kütüphane eklendi.
import threading #Çoklu işlem için gereken kütüphane eklendi.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Bağlantı türü ve özellikleri belirtildi.
serverRunning = True #Sunucunun çalıştığı belirtildi.
ip = "127.0.0.1" #İp local ip olarak girildi.
port = 1234 #Herhangi bir port girildi. Önemli değil.

clients = {} #Client bir sözlük olarak belirtildi.

s.bind((ip, port)) #Bağlantı açıldı.
s.listen() #Gelecek bağlantıların artık beklenmekte.
print('Server Ready...') #Anlaşılması için sunucunun hazır olduğu belirtildi.
print('Ip Address of the Server::%s'%ip) #Bağlantı için gereken ip adresi yazıldı.

def handleClient(client, uname): #Bağlantı alındığında neler yapılması gerektiği belirlendi.
    clientConnected = True #Client'in bağlandığı anlaşıldı.
    keys = clients.keys() #Client'ten gelen verinin anahtarları belirlendi.
    help = 'There are four commands in Messenger\n1::**chatlist=>gives you the list of the people currently online\n2::**quit=>To end your session\n3::**broadcast=>To broadcast your message to each and every person currently present online\n4::Add the name of the person at the end of your message preceded by ** to send it to particular person'
    #Yardım için neler gerektiği belirtildi.

    while clientConnected: #Client bağlandığında yapılacaklar belirtildi.
        try: #Denenmesi gerekenler açıklandı.
            msg = client.recv(1024).decode('ascii') #Mesaj kısaca msg olarak belirtildi. Ayrıca 1024 kilobyte boyutunda ve ascii metin türünde alınacağı belirtildi.
            response = 'Number of People Online\n' #Geri dönüt açıklandı.
            found = False #Bulunma işinin henüz olmadığı belirtilir.
            if '**chatlist' in msg: #Eğer gelen mesaj **chatlist ise
                clientNo = 0 #Client numarası 0 olarak belilendi.
                for name in keys: #Belirlenen anahtarlar arasından isimler arasında işlem yapılacağı gösterildi.
                    clientNo += 1 #Her bir kullanıcıda Client numarasının 1 artacağı belirlendi.
                    response = response + str(clientNo) +'::' + name+'\n' #Geri dönüt kullanıcı adları ve sayısının da eklenmesiyle tekrar düzenlendi.
                client.send(response.encode('ascii')) #Dönüt server üzerinden kullanıcılara gönderildi.
            elif '**help' in msg: #Eğer gelen mesaj **help ise
                client.send(help.encode('ascii')) # Help adlı geri dönüt server üzerinden kullanıcılara gönderildi.
            elif '**broadcast' in msg: #Eğer gelen mesaj **broadcast ise
                msg = msg.replace('**broadcast','') #Mesaj gönderilmek üzere tekrar düzenlendi.
                for k,v in clients.items(): #Gelen tüm veriler incelendi.
                    v.send(msg.encode('ascii')) #Mesaj tüm kullanıcılara gönderildi.
            elif '**quit' in msg: #Eğer gelen mesaj **quit ise
                response = 'Stopping Session and exiting...' #Dönüt tekrardan ayarlandı.
                client.send(response.encode('ascii')) #Dönüt kullanıcılara server üzerinden gönderildi.
                clients.pop(uname) #Client'ten kullanıcı adı silindi.
                print(uname + ' has been logged out') #Ekrana kullanıcının çıktığını belirten bir dönüt gösterildi.
                clientConnected = False #Client ile bağlantı kesildi.
            else: #Mesaj yukarıdakilerden hiçbiri değil ise
                for name in keys: #Belirlenen anahtarlar arasından isimler ile işlem yapılacağı gösterildi.
                    if('**'+name) in msg: #Eğer mesajda ** yanında isim de var ise
                        msg = msg.replace('**'+name, '') #Mesaj tekrar gönderilmek üzere düzenlendi.
                        clients.get(name).send(msg.encode('ascii')) #Mesaj belirtilen kişiye gönderildi.
                        found = True #Bulunma işinin yapıldığını belirtir.
                if(not found): #Eğer bulunmadıysa
                    client.send('Trying to send message to invalid person.'.encode('ascii')) #Kullanıcın mesajını geçersiz birine attığı konusunda uyarı mesajı çıkartıldı.
        except: #Denenecekler dışında herhangi bir durumda
            clients.pop(uname) #Client'ten kullanıcı adı silindi.
            print(uname + ' has been logged out') #Ekrana kullanıcının çıktığını beliten bir dönüt gösterildi.
            clientConnected = False #Client ile bağlantı kesildi.


        


while serverRunning: #Sunucu çalıştığı sürece
    client, address = s.accept() #Client ve adres doğrulandı.
    uname = client.recv(1024).decode('ascii') #Kullanıcı adı alındı.
    print('%s connected to the server'%str(uname)) #Bağlanan kullanıcıların ismi gösterildi.
    client.send('Welcome to Messenger. Type **help to know all the commands'.encode('ascii')) #Katılan kullanıcıya giriş cümlesi gösterildi.
    
    if(client not in clients): #Eğer client clients adındaki sözlükte değil ise
        clients[uname] = client #Kullanıcı adı cliente eşitlendi.
        threading.Thread(target = handleClient, args = (client, uname, )).start() #Çoklu işlem için gereken altyapı sağlandı.
        

