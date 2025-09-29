from enum import Enum

class OpCode(Enum):
    RRQ = 1
    DAT = 3
    ACK = 4
    ERR = 5

SOCKET_BUFFER = 2048