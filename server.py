"""
Description: Multi client communication using socket and threading modules
And to store that communicated messages into tessrac database using MySQL
Author: Sonia
Position: Junior Software Engineer

"""
import threading
import socket
import _thread
        
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

def receive():
    global client_length
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        client_length += 1
        aliases.append(alias)
        clients[client_length] = client 
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        message = clients[client_length].recv(1024).decode('utf-8')
        if message == "":
            continue
        client, data = message.split(" ",1)
        message = clients[client_length].recv(1024).decode('utf-8')
        # router(clients[client_length],'{} has connected to the chat room with client ID: {}'.format(alias,client_length))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client_length,))
        thread.start()



if __name__ == "__main__":
    receive()
