import os,random
from socket import *
SERVER = '127.0.0.1'
PORT = 2121
DIR_INIT ='root'
os.chdir(DIR_INIT)
DIR_HOME = os.getcwd()

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

def handle_pwd():
    return  '/' if os.getcwd() == DIR_HOME else os.getcwd()[len(DIR_HOME):].replace("\\","/")

def handle_cd(dir):
    if os.path.exists(dir):
        lastDir = os.getcwd()
        os.chdir(dir)
        if os.getcwd().startswith(DIR_HOME):
            response = 'Changed directory.'
        else:
            os.chdir(lastDir)
            response = "Access denied! couldn't change directory"
    else:
        response = 'The directory does not exist!\n'
    print(response)
    return response

def build_data_channel():
    port = random.randint(3000, 50000)
    dChannel = socket(AF_INET, SOCK_STREAM)
    dChannel.bind((SERVER, port))
    dChannel.listen()
    return dChannel , str(port)

def handle_dl(connection , file):
    if file in os.listdir():
        print('Sending...')
        data_channel,data_port = build_data_channel()
        send_response(connection , data_port)

        data_channel_conn, addr = data_channel.accept()
        if os.path.exists(file):
            with open(file, 'rb') as file:
                data = file.read()
                data_channel_conn.send(data)
            print('File sent successfully')
            data_channel_conn.close()
            data_channel.close()
            print('\nClosing Data Channel ...')
            response =  'File download successfully'
        else:
            data_channel_conn.close()
            response = "The file doesn't exist"
    else:
        response = "404"
    return response


def handle_request(connection):
    cmd = connection.recv(1024).decode()
    response = cmd
    print("Received Command: " + cmd)
    if cmd == 'list':
        response = handle_list()
    elif cmd == 'pwd':
        response = handle_pwd()
    elif cmd.startswith("cd"):
        response = handle_cd(cmd[3:])
    elif cmd.startswith("dwld"):
        response = handle_dl(connection,cmd[5:])
        if response == 'File download successfully':
            return
    elif cmd == 'quit':
        response = ''
        send_response(connection, response)
        connection.close()
        exit()

    send_response(connection,response )

def send_response(connection ,res):
    connection.send(res.encode())

conn, addr = server.accept()
while True:
    try:
        handle_request(conn)
    except Exception as e:
        print("Connection Lost!")
        conn.close()
        break
