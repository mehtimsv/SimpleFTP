from socket import *
SERVER = '127.0.0.1'
PORT = 2121

def cmd_help():
    print(
        """
List of the commands: 
help            : Show the help
list            : List files
pwd             : Show current dir
cd dir_name     : Change directory
dwld file_path  : Download a file
quit            : Exit
    """)

def cmd_exit():
    print("Good Bye!")
    client.close()
    exit()

def downloading(port, file):
    dChannel = socket(AF_INET, SOCK_STREAM)
    try:
        dChannel.connect((SERVER, int(port)))
    except Exception as e:
        print("Can't Connect! something's wrong with %s:%d. Exception is %s" % (SERVER, port, e))

    print('Downloading...')
    data = dChannel.recv(1048576)
    with open(file, 'wb') as f:
        f.write(data)
        print('The file downloaded :)')
    dChannel.close()
    return True

def send_request(cmd):
    client.sendall(cmd.encode())
    return client.recv(1024)

def handle_response(cmd, res):
    if cmd.startswith("dwld"):
        port = res.decode()
        if port == '404':
            print("Error 404. The file doesn't exist")
        else:
            downloading(port, cmd[5:])
    elif cmd == "quit":
        cmd_exit()
    else:
        print(res.decode())


print("Trying to connect...")
client = socket(AF_INET, SOCK_STREAM)
try:
    client.connect((SERVER, PORT))
    print("Connection successful ;)")
    cmd_help()
except Exception as e:
    print("Can't Connect! something's wrong with %s:%d. Exception is %s" % (SERVER, PORT, e))
    exit()

while True:
    cmd = input("$cmd: ").lower()
    if cmd == 'help':
        cmd_help()
    elif cmd.split(" ")[0] in ["list", "pwd", "cd", "dwld", "quit"]:
        handle_response(cmd, send_request(cmd))
    else:
        print("This command does not exist")
