import socket
from scapy.all import *

SRC_PORT = 65000

msg = ""
triplets_received = 0
total_triplets = 0
stop = False

def filter(packet):
    if packet.haslayer(TCP) and packet[TCP].sport == SRC_PORT and packet[TCP].flags == "SA":
        msg += packet[TCP].reserved.decode()
        count += 1
        if count == packet[TCP].ack:
            stop = True

def receive_message(port: int) -> str:
    """Receive *hidden* messages on the given TCP port.

    As Winston sends messages encoded over the TCP metadata, re-implement this
    function so to be able to receive the messages correctly.

    Notes:
    1. Use `SRC_PORT` as part of your implementation.
    """
    listener = socket.socket()
    #listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        listener.bind(('', port))
        listener.listen(1)
        connection, address = listener.accept()
        
        try:                
            sniff(iface=get_if_list(), prn=filter, stop_filter=lambda packet: stop)
            return msg
            
        finally:
            connection.close()
    finally:
        listener.close()


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    message = receive_message(1984)
    print('received: %s' % message)


if __name__ == '__main__':
    main()
