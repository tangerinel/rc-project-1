from helpers.constants import OpCode as op_codes
import pickle
from ACK_handler import send_ACK

def send_DAT (connSocket, blockNum, data):
    data_packet = {
        "opcode": op_codes.DAT,
        "block#": blockNum,
        "size": len(data),
        "data": data
    }
    connSocket.send(pickle.dumps(data_packet))


def handle_DAT(data):
    print("Received DAT block", data.get("block#"))
    return

def receive_DAT (connSocket, sockBuffer):
    while True:
        data = connSocket.recv(sockBuffer)
        if not data:
            break;
        req = pickle.loads(data)
        if req.get("opcode") != op_codes.DAT:
            print("Expected DAT packet")
            break;
        if req.get("size") > 0:
            print(req.get("data").decode("ascii"))
            send_ACK(connSocket, req.get("block#"))
        if req.get("size") <= 0:
            break;