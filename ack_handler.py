import pickle
from helpers.constants import OpCode

def receive_and_validate_ack(connSocket, sockBuffer, expectedBlockNum):
      data = connSocket.recv(sockBuffer)
      if not data:
          print("Peer closed before ACK")
          return False
      res = pickle.loads(data)
      return res.get("opcode") == OpCode.ACK and res.get("block#") == expectedBlockNum


def send_ack(connSocket, blockNum):
    ack_packet = {
        "opcode": OpCode.ACK,
        "block#": blockNum
    }
    connSocket.send(pickle.dumps(ack_packet))