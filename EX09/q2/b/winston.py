import socket
from Crypto.Cipher import AES

import base64
import hashlib
from Crypto import Random


def send_message(ip: str, port: int):
    """Send an *encrypted* message to the given ip + port.

    Julia expects the message to be encrypted, so re-implement this function accordingly.

    Notes:
    1. The encryption is based on AES.
    2. Julia and Winston already have a common shared key, just define it on your own.
    3. Mind the padding! AES works in blocks of 16 bytes.
    """
    
    connection = socket.socket()
    try:
        connection.connect((ip, port))
        #connection.send(b'I love you')
        msg = 'I love you'
        
        # credit: https://stackoverflow.com/questions/12524994/encrypt-and-decrypt-using-pycrypto-aes-256
        block_size = 16
        key = hashlib.sha256('This is Julias and Winstons key'.encode()).digest()
        
        # PKCS7 padding : https://stackoverflow.com/questions/12524994/encrypt-and-decrypt-using-pycrypto-aes-256
        # appending N bytes with the value of chr(N), where N is the number of bytes required to make the final block of data the same size as the block size
        N = (block_size-len(msg)) % block_size
        raw = msg + N * chr(N) 
        
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        connection.send(base64.b64encode(iv + cipher.encrypt(raw.encode())))
               
    finally:
        connection.close()


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    send_message('127.0.0.1', 1984)


if __name__ == '__main__':
    main()
