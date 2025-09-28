from helpers.list_dir import list_dir
import os, pickle
from helpers.constants import OpCode as op_codes, sockBuffer
from ACK_handler import receive_and_validate_ACK
from DAT_handler import send_DAT
from ERR_handler import send_ERR

def send_dir_listing(connSocket, dirList):
    blockNum = 1
    print("Sending directory listing with", len(dirList), "items")
    for filename in dirList:
        send_DAT(connSocket, blockNum, filename.encode("ascii"))
        response = receive_and_validate_ACK(connSocket, sockBuffer, blockNum )
        if not response:
            send_ERR(connSocket, f"Failed to receive ACK for block {blockNum}")
            return
        blockNum += 1
    
    send_DAT(connSocket, blockNum, b"" )
    response = receive_and_validate_ACK(connSocket, sockBuffer, blockNum )
    if not response:
        send_ERR(connSocket, f"Failed to receive ACK for block {blockNum}")
        return
    return


def send_file_contents(connSocket, base_dir, filename):
    filepath = os.path.join(base_dir, filename)
    blockNum = 1
    try:
        with open(filepath, "rb") as f:
            while True:
                data = f.read(512)
                send_DAT(connSocket, blockNum, data)
                response = receive_and_validate_ACK(connSocket, sockBuffer, blockNum )
                if not response:
                    send_ERR(connSocket, f"Failed to receive ACK for block {blockNum}")
                    break
                if len(data) <= 0:
                    break
                blockNum += 1
    except Exception as e:
        send_ERR(connSocket, f"Error reading file '{filename}': {e}")
        return
    return




def handle_RRQ_Request(connSocket, data):
    base_dir = os.getcwd()
    filename = data.get("filename", "")
    dirList = list_dir(base_dir)
    if filename == "":
       try:
           send_dir_listing(connSocket, dirList)
       except Exception as e:
           send_ERR(connSocket, f"Error sending directory listing: {e}")
           return
    else:
        if filename not in dirList:
            print(f"File '{filename}' not found")
            send_ERR(connSocket, f"File '{filename}' not found")
            return
        send_file_contents(connSocket, base_dir, filename)


def send_RRQ_Request (connSocket, filename):
    rrq_packet = {
        "opcode": op_codes.RRQ,
        "filename": filename
    }
    connSocket.send(pickle.dumps(rrq_packet))