import socket
from scapy.all import *

SRC_PORT = 65000


def send_message(ip: str, port: int):
    """Send a *hidden* message to the given ip + port.

    Julia expects the message to be hidden in the TCP metadata, so re-implement
    this function accordingly.

    Notes:
    1. Use `SRC_PORT` as part of your implementation.
    """
      
    connection = socket.socket()
    
    try:
        connection.connect((ip, port))
        #connection.send(b'I love you')
        
        msg = "I love you"
        triplets = [ord(c) for c in msg] 

        # Create the SYN/ACK packets with the reserved bits containing the triplets
        packets = []
        for seq_num, triplet in enumerate(triplets):
            packet = IP(dst=ip) / TCP(dport=port, sport=SRC_PORT, flags="SA", reserved=triplet, ack=len(triplets))
            packet[TCP].seq = seq_num
            connection.send(bytes(packet))
   
    finally:
        connection.close()


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    send_message('127.0.0.1', 1984)


if __name__ == '__main__':
    main()
