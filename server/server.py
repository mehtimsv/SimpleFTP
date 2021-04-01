from socket import *
SERVER = '127.0.0.1'
PORT = 2121
print("Trying to create server...")
try:
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((SERVER, PORT))
    server.listen()
    print("Server created successfully ;)")
except Exception as e:
    print("Can't Create Server! something's wrong with %s:%d. Exception is %s" % (SERVER, PORT, e))
    exit()


def handle_request(connection):
    send_response(connection, connection.recv(1024).decode())

def send_response(connection ,res):
    connection.send(res.encode())

conn, addr = server.accept()
while True:
    handle_request(conn)

conn.close()