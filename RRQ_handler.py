from helpers.list_dir import list_dir
import os, pickle
from helpers.constants import OpCode as op_codes, sockBuffer
from ACK_handler import receive_and_validate_ACK
from DAT_handler import send_DAT

def send_dir_listing(connSocket, dirList):
    blockNum = 1
    for filename in dirList:
        send_DAT(connSocket, blockNum, filename.encode("ascii"))
        response = receive_and_validate_ACK(connSocket, sockBuffer, blockNum )
        if not response:
            return
        blockNum += 1
    
    send_DAT(connSocket, blockNum, b"" )
    response = receive_and_validate_ACK(connSocket, sockBuffer, blockNum )
    if not response:
        return
    return





def handle_RRQ(connSocket, data):
    base_dir = os.getcwd()
    filename = data.get("filename", "")
    if filename == "":
       dirList = list_dir(base_dir)
       try:
           send_dir_listing(connSocket, dirList)
       except Exception as e:
            print("Error sending directory listing:", e)


def send_RRQ (connSocket, filename):
    rrq_packet = {
        "opcode": op_codes.RRQ,
        "filename": filename
    }
    connSocket.send(pickle.dumps(rrq_packet))