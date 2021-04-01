import os
from socket import *
SERVER = '127.0.0.1'
PORT = 2121
DIR_HOME = 'root'
os.chdir(DIR_HOME)
DIR_NOW = os.getcwd()

print("Trying to create server...")
try:
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((SERVER, PORT))
    server.listen()
    print("Server created successfully ;)")
except Exception as e:
    print("Can't Create Server! something's wrong with %s:%d. Exception is %s" % (SERVER, PORT, e))
    exit()

def handle_list():
    sumOfFileSize = 0
    ls = ''
    for f in os.listdir():
        sizeOfFile = os.path.getsize(f)
        ls += "{}  {} - {}b\n".format(">    " if os.path.isdir(f) else "     " , f ,sizeOfFile)
        sumOfFileSize += sizeOfFile

    return ls + '\nTotal Directory Size: {}b '.format(sumOfFileSize)

def handle_request(connection):
    cmd = connection.recv(1024).decode()
    response = cmd
    print(cmd)
    if cmd == 'list':
        response = handle_list()

    send_response(connection,response )

def send_response(connection ,res):
    connection.send(res.encode())

conn, addr = server.accept()
while True:
    handle_request(conn)

conn.close()