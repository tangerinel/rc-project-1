from helpers.constants import OpCode as op_codes
import pickle

def send_ERR(connSocket,  errorMsg):
    err_packet = {
        "opcode": op_codes.ERR,
        "error": errorMsg
    }
    connSocket.send(pickle.dumps(err_packet))
