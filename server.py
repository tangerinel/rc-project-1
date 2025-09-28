
from socket import *
import pickle, threading
from helpers.constants import OpCode as op_codes, sockBuffer
from rrq_handler import handle_rrq_request
from dat_handler import send_dat
from ack_handler import receive_and_validate_ack
import sys


def handle_client(connSocket, addr):
    send_dat(connSocket, 1, f"Welcome to {connSocket.getsockname()[0]} file server".encode("ascii"))
    res = receive_and_validate_ack(connSocket, sockBuffer, 1 )
    try:
        if not res: 
            return
        while True:
            received = connSocket.recv(sockBuffer)
            if not received:
                break;
            data = pickle.loads(received)
            op = data.get("opcode")
            if op == op_codes.RRQ:
                handle_rrq_request(connSocket, data)
            else:
                print("Unknown opcode from", addr)
                break
    except Exception as e:
        print("Error handling client:", e)
    finally:
        connSocket.close()



def main(port):

    serverSocket = socket(AF_INET,SOCK_STREAM)   # create TCP welcoming socket

    try:
        serverSocket.bind(("", port))   
        serverSocket.listen(2)               
        print("Server is running")       
        try:
             while True:
                connSocket, addr = serverSocket.accept()    # waits for incoming requests:
                                                          # new socket created on return
                threading.Thread(target=handle_client, args=(connSocket, addr), daemon=True).start()
        except KeyboardInterrupt:
            print("Server stopping")
    except OSError:
        print("Unable to start server")
        return
    finally:
        serverSocket.close()

   


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Inavlid number of arguments!\nUsage: python server.py [port]")
        sys.exit(1)
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Port must be an integer")
        sys.exit(1)

    main(port)