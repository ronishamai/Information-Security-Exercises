import math
from scapy.all import *


LOVE = 'love'
unpersons = set()


def spy(packet):
    """Check for love packets and encrypted packets.

    For each packet containing the word 'love', or a packed which is encrypted,
    add the sender's IP to the `unpersons` set.

    Notes:
    1. Use the global LOVE as declared above.
    """
    
    unpersons.add(packet[IP].src) if (packet.haslayer(TCP) and ((bytes(packet[TCP].payload).decode().find(LOVE) != -1) or (shannon_entropy(bytes(packet[TCP].payload).decode()) > 3))) else None 

def shannon_entropy(string: str) -> float:
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    distribution = [float(string.count(c)) / len(string)
                    for c in set(string)]
    return -sum(p * math.log(p) / math.log(2.0) for p in distribution)


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    sniff(iface=get_if_list(), prn=spy)


if __name__ == '__main__':
    main()
