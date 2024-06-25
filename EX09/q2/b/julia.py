import socket
from Crypto.Cipher import AES

import base64
import hashlib
from Crypto import Random


def receive_message(port: int) -> str:
    """Receive *encrypted* messages on the given TCP port.

    As Winston sends encrypted messages, re-implement this function so to
    be able to decrypt the messages.

    Notes:
    1. The encryption is based on AES.
    2. Julia and Winston already have a common shared key, just define it on your own.
    3. Mind the padding! AES works in blocks of 16 bytes.
    """

    listener = socket.socket()
    try:
        listener.bind(('', port))
        listener.listen(1)
        connection, address = listener.accept()
        try:
            #msg = connection.recv(1024).decode("latin-1")
            
            # credit: https://stackoverflow.com/questions/12524994/encrypt-and-decrypt-using-pycrypto-aes-256
            block_size = 16
            key = hashlib.sha256('This is Julias and Winstons key'.encode()).digest()
            
            enc = base64.b64decode(connection.recv(1024))
            iv = enc[:AES.block_size]
            cipher = AES.new(key, AES.MODE_CBC, iv)        
            msg = cipher.decrypt(enc[AES.block_size:])
            
            # PKCS7 padding: https://stackoverflow.com/questions/12524994/encrypt-and-decrypt-using-pycrypto-aes-256
            # appending N bytes with the value of chr(N), where N is the number of bytes required to make the final block of data the same size as the block size
            N = ord(msg[-1:])
            msg = msg[:-N].decode('utf-8')
            
            return msg

            
        finally:
            connection.close()
    finally:
        listener.close()


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    message = receive_message(1984)
    print('received: %s' % message)


if __name__ == '__main__':
    main()
