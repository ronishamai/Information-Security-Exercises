from scapy.all import *


def on_packet(packet):
    """Implement this to send a SYN ACK packet for every SYN.

    Notes:
    1. Use *ONLY* the `send` function from scapy to send the packet!
    """
    
    if packet.haslayer(TCP):
        if packet[TCP].flags == 'S': # for every SYN
            send(IP(dst=packet[IP].src) / TCP(dport=packet[TCP].sport, sport=packet[TCP].dport, flags='SA')) # send a SYN ACK packet

def main(argv):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    sniff(prn=on_packet)


if __name__ == '__main__':
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    import sys
    sys.exit(main(sys.argv))
