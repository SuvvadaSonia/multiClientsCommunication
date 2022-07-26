"""
Description: Two way socket communication using socket and threading modules
And to store that communicated messages into tessrac database using MySQL
Author: Sonia
Position: Junior Software Engineer

"""
import queue
import threading
import socket
from time import sleep

host = socket.gethostname()
port = 3003
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = {}
aliases = []

# def router(client,data):
#     if client in clients:
#         clients[client].send(data.encode('utf-8'))

# Function to handle clients'connections


def handle_client(client_length):
    while True:
        try:
            message = clients[client_length].recv(1024).decode('utf-8')
            if message == "":
                continue
            client, data = message.split(" ",1)
            message = clients[client_length].recv(1024).decode('utf-8')
        except:
            # del clients[client]
            client.close()
            alias = aliases[client-1]
            # router(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break


# Main function to receive the clients connection

client_length = 0
clientQ = queue.Queue()

def router():

    clients = {}

    while True:
        while True:
            try:
                _client = clientQ.get_nowait()
                clients.update(dict(_client))
                print(clients)
                if clientQ.empty():
                    print('Q emty')
                    break
            except queue.Empty:
                break

        sleep(.5)
        try:
            for client, conn in clients.items():
                msg = conn.recv(1024).decode('utf-8')
                print(msg)
                if msg == "":
                    continue
                receiver, msg = msg.split(':',1)
                if receiver in clients:
                    clients[receiver].send(msg.encode('utf-8'))
                    print(f"{msg} - sent to {receiver}")
                else:
                    print(f"user not in list")
        except RuntimeError:
            continue

routerThread = threading.Thread(target=router)
# routerThread.setDaemon(True)
routerThread.start()
def receive():
    global client_length
    print('Server is running and listening ...')


    while True:
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        msg = client.recv(1024).decode('utf-8')
        print(msg)
        if msg == 'register':
            client.send('alias?'.encode('utf-8'))
            alias = client.recv(1024).decode('utf-8')
            clientQ.put({alias:client})

            print(f'{alias} has joined and username is - {alias}'.encode('utf-8'))
        # else:
        #     receiver, msg = msg.split(',',1)
        #     if receiver in clients:
        #         clients[receiver].send(msg).encode('utf-8')
        #     else:
        #         print(f"user not in list")



if __name__ == "__main__":
    receive()