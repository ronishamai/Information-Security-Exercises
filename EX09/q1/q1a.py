from scapy.all import *
from typing import List, Iterable


OPEN = 'open'
CLOSED = 'closed'
FILTERED = 'filtered'


def generate_syn_packets(ip: str, ports: List[int]) -> list:
    """
    Returns a list of TCP SYN packets, to perform a SYN scan on the given
    TCP ports.

    Notes:
    1. Do NOT add any calls of your own to send/receive packets.
    """
    TCP_SYN_packets = []
    
    for port in ports:
        packet = IP(dst=ip)/TCP(dport=port)
        TCP_SYN_packets.append(packet)
    
    return TCP_SYN_packets


def analyze_scan(ip: str, ports: List[int], answered: Iterable, unanswered: Iterable) -> dict:
    """Analyze the results from `sr` of SYN packets.

    This function returns a dictionary from port number (int), to
    'open' / 'closed' / 'filtered' (strings), based on the answered and unanswered
    packets returned from `sr`.

    Notes:
    1. Use the globals OPEN / CLOSED / FILTERED as declared above.
    """
    
    # Assuming that all the relevant packets will be accounted for in the answered and unanswered
    # Credit https://nmap.org/book/synscan.html
    
    results = dict()
 
    for packet in unanswered:
        
        if packet.haslayer('TCP'): # TCP packet            
            port = packet[0].getlayer('TCP').dport # Port NUmber
            results[port] = FILTERED # No response received (even after retransmissions) indicates filtered port

    
    for packet in answered:
                
        if packet[0].haslayer('TCP'): # TCP packet
            
            port = packet[0].getlayer('TCP').dport # Port NUmber
            flags = packet[0].getlayer('TCP').flags # Flags
            
            if flags == 'SA': # ‘SA’ flags indicates open ports 
                results[port] = OPEN
            if flags == 'RA': # ‘RA’ flags indicates closed ports
                results[port] = CLOSED
                
        if packet[0].haslayer('ICMP') and packet[0].getlayer('ICMP').type == 3 and packet[0].getlayer('ICMP').code in [1, 2, 3, 9, 10, 13]: # ICMP packet
            port = packet[0].getlayer('ICMP').dport # Port NUmber
            results[port] = FILTERED # ICMP unreachable error, indicates filtered port
        
        print(results)
    
    return results    


def stealth_syn_scan(ip: str, ports: List[int], timeout: int):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    packets = generate_syn_packets(ip, ports)
    answered, unanswered = sr(packets, timeout=timeout)
    return analyze_scan(ip, ports, answered, unanswered)


def main(argv):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    if not 3 <= len(argv) <= 4:
        print('USAGE: %s <ip> <ports> [timeout]' % argv[0])
        return 1
    ip = argv[1]
    ports = [int(port) for port in argv[2].split(',')]
    if len(argv) == 4:
        timeout = int(argv[3])
    else:
        timeout = 5
    results = stealth_syn_scan(ip, ports, timeout)
    for port, result in results.items():
        print('port %d is %s' % (port, result))


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
