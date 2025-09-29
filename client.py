
from socket import *
import pickle
from helpers.constants import OpCode, SOCKET_BUFFER
from rrq_handler import send_rrq_request
from dat_handler import receive_dat
from ack_handler import send_ack
import sys
import os
from helpers.list_dir import list_dir

def is_valid_get_cmd(local_filename):

    files = list_dir(os.getcwd())
    if local_filename in files:
       print(f"Local file '{local_filename}' already exists")
       return False
    return True



def main(host, port):
    clientSocket = socket(AF_INET,SOCK_STREAM)       # create TCP socket

    try:
        clientSocket.connect((host, port))   # open TCP connection
        print("Connect to server")          
    except OSError:
        print("Unable to connect with the server")
        return

    # manage initial handshake
    handshake = pickle.loads(clientSocket.recv(SOCKET_BUFFER))
    if handshake.get("opcode") != OpCode.DAT or handshake.get("block#") != 1:
        print("Handshake failed")
        clientSocket.close()
        return
    send_ack(clientSocket,  handshake.get("block#"));

    print(handshake.get("data").decode("ascii"))


    while True:
        cmd = input("Enter command (dir, get <remote_filename> <local_filename>, end): ").strip()
        if cmd == "end":
            clientSocket.close()
            print("Connection close, client ended")
            break;
        elif cmd == "dir":
            send_rrq_request(clientSocket, "")
            res = receive_dat(clientSocket, SOCKET_BUFFER, True)
            for item in res:
                print(item.decode("ascii"))
        elif cmd.startswith("get"):
            parts = cmd.split(" ", 2)
            if len(parts) != 3:
                print("Invalid number of arguments\nExpected: get <remote_filename> <local_filename>")
                continue
            remote_filename = parts[1]
            local_filename = parts[2]
            if not is_valid_get_cmd(local_filename):
                continue
            send_rrq_request(clientSocket, remote_filename)
            res = receive_dat(clientSocket, SOCKET_BUFFER)
            if len(res) > 0:
                try:
                    with open(local_filename, "wb") as f:
                        for chunk in res:
                            f.write(chunk)
                    print("File transfer completed")
                except Exception as e:
                    print(f"Error saving file: {e}")
        else:
            print("Unknown command")
            continue;
            


    clientSocket.close()            # close TCP connection

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Inavlid number of arguments!\nUsage: python client.py [server_ip][server_port]")
        sys.exit(1)
    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Port must be an integer"); sys.exit(1)

    main(host, port)