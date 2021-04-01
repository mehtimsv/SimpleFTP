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
    exit()

def send_request(cmd):
    client.send(cmd.encode())
    return client.recv(1024)

def handle_response(res):
    print(res)


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
    cmd = input("$cmd: ")
    if cmd == 'help':
        cmd_help()
    elif cmd == 'quit':
        cmd_exit()
    else:
        handle_response(send_request(cmd))
