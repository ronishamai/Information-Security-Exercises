from scapy.all import *


LOVE = 'love'
unpersons = set()


def spy(packet):
    """Check for love packets.

    For each packet containing the word 'love', add the sender's IP to the
    `unpersons` set.

    Notes:
    1. Use the global LOVE as declared above.
    """
    
    unpersons.add(packet[IP].src) if (packet.haslayer(TCP) and bytes(packet[TCP].payload).decode().find(LOVE) != -1) else None # tracks TCP packets containing the word love, and adds the senders IP to the unpersons set

def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    sniff(iface=get_if_list(), prn=spy)


if __name__ == '__main__':
    main()
