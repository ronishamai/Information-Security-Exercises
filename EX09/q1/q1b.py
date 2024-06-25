import time
import os
from scapy.all import *


WINDOW = 60
MAX_ATTEMPTS = 15


# Initialize your data structures here
ip_SYN_times_dict = dict()


blocked = set()  # We keep blocked IPs in this set


def on_packet(packet):
    """This function will be called for each packet.

    Use this function to analyze how many packets were sent from the sender
    during the last window, and if needed, call the 'block(ip)' function to
    block the sender.

    Notes:
    1. You must call block(ip) to do the blocking.
    2. The number of SYN packets is checked in a sliding window.
    3. Your implementation should be able to efficiently handle multiple IPs.
    """

    if packet.haslayer(TCP) and packet[TCP].flags == 'S':  # SYN packet
        ip = packet[IP].src
        
        if ip not in ip_SYN_times_dict:
            ip_SYN_times_dict[ip] = [] 
            
        else:
            curr = time.time()
            SYNs_in_the_last_60 = [curr]
            for SYN_time in ip_SYN_times_dict[ip]:
                if SYN_time >= curr - WINDOW:
                    SYNs_in_the_last_60.append(SYN_time)
            ip_SYN_times_dict[ip] = SYNs_in_the_last_60
            
        if len(ip_SYN_times_dict[ip]) > MAX_ATTEMPTS:
            block(ip)         
                

def generate_block_command(ip: str) -> str:
    """Generate a command that when executed in the shell, blocks this IP.

    The blocking will be based on `iptables` and must drop all incoming traffic
    from the specified IP."""
    
    return f"iptables -A INPUT -s {ip} -j DROP" # Formatted string which combines the command and the fiven ip.


def block(ip):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    os.system(generate_block_command(ip))
    blocked.add(ip)


def is_blocked(ip):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    return ip in blocked


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    sniff(prn=on_packet)


if __name__ == '__main__':
    main()
