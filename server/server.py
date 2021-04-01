from socket import *
SERVER = '127.0.0.1'
PORT = 2121

try:
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((SERVER, PORT))
    server.listen(5)
except Exception as e:
    print("Can't Create Server! something's wrong with %s:%d. Exception is %s" % (SERVER, PORT, e))
    exit()


def handle_request(connection):
    send_response(connection, connection.recv(1024).decode())

def send_response(connection ,res):
    connection.send(res.encode())


while True:
    conn, addr = server.accept()
    handle_request(conn)
