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


def receive_DAT (connSocket, sockBuffer, isDirListing=False):
    res = []
    expectedBlockNum = 1
    while True:
        data = connSocket.recv(sockBuffer)
        if not data:
            break;
        req = pickle.loads(data)
        if req.get("opcode") != op_codes.DAT:
            if req.get("opcode") == op_codes.ERR:
                print("Received ERR code", req.get("error"))
            else:
                print("Expected DAT packet")
            connSocket.close()
            break;
        if req.get("block#") != expectedBlockNum:
            print("Unexpected block number, expected", expectedBlockNum, "got", req.get("block#"))
            connSocket.close()
            break;
        if req.get("size") == 512 or isDirListing and req.get("size") > 0:
            res.append(req.get("data"))
            send_ACK(connSocket, req.get("block#"))
            expectedBlockNum += 1
        if req.get("size") <= 512 and not isDirListing or isDirListing and req.get("size") == 0:
            res.append(req.get("data"))
            send_ACK(connSocket, req.get("block#"))
            break;
    return res