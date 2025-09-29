from helpers.constants import OpCode
import pickle

def send_err(connSocket,  errorMsg):
    err_packet = {
        "opcode": OpCode.ERR,
        "error": errorMsg
    }
    connSocket.send(pickle.dumps(err_packet))
