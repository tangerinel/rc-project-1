
from socket import *
import pickle
from helpers.constants import OpCode as op_codes
from RRQ_handler import send_RRQ
from DAT_handler import receive_DAT
from ACK_handler import send_ACK
import sys

serverName = "localhost"            # server name
serverPort = 12000                  # socket server port number
sockBuffer = 2048                   # socket buffer size

def main(host, port):
    clientSocket = socket(AF_INET,SOCK_STREAM)       # create TCP socket

    try:
        clientSocket.connect((host, port))   # open TCP connection
        print("Connect to server")          
    except OSError:
        print("Unable to connect with the server")
        return

    #manage initial handshake
    handshake = pickle.loads(clientSocket.recv(sockBuffer))
    if handshake.get("opcode") != op_codes.DAT or handshake.get("block#") != 1:
        print("Handshake failed")
        clientSocket.close()
        return
    send_ACK(clientSocket,  handshake.get("block#"));

    print(handshake.get("data").decode("ascii"))


    while True:
        cmd = input("Enter command (dir, get <filename>, end): ").strip()
        if cmd == "end":
            clientSocket.close()
            print("Connection closed.")
            break;
        elif cmd == "dir":
            send_RRQ(clientSocket, "")
            receive_DAT(clientSocket, sockBuffer)
        else:
            print("Unknown command")
            break;
            


    clientSocket.close()            # close TCP connection

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)
    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Port must be an integer"); sys.exit(1)
    main(host, port)