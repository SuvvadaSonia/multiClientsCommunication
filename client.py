"""
Description: Two way socket communication using socket and threading modules
And to store that communicated messages into tessrac database using MySQL
Author: Sonia
Position: Junior Software Engineer

"""
import threading
import socket
import datetime
import random
import mysql.connector


con = mysql.connector.connect(host="localhost", user="root",password="Jagson@5355" ,database="tessrac")
cur = con.cursor()

alias = input('Your good name: ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
h = socket.gethostname()
client.connect((h, 3003))


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        mess = input()
        num = random.randint(5,5000)
        message = f'{alias}: {mess}'
        client.send(message.encode('utf-8'))
        
        date_time = datetime.datetime.now()
        query = "Insert into communication values ({},'{}','{}','{}',1,'{}','teja')".format(num,mess,date_time,date_time,alias)
        cur.execute(query)
        con.commit()


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()

