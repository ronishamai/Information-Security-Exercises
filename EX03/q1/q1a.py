def check_message(path: str) -> bool:
    """
    Return True if `msgcheck` would return 0 for the file at the specified path,
    return False otherwise.
    :param path: The file path.
    :return: True or False.
    """
    with open(path, 'rb') as reader:
        # Read data from the file, do whatever magic you need
        
        # reads msg
        msg = reader.read()
        
        # init args
        arg_0 = msg[0] # msg len
        var_4 = arg_0 
        var_9 = msg[1] # xor msg val
        var_A = 0x19 # xor key
        var_8 = 2 # loop variable (over the msg)
        
        msg = msg[:2+arg_0]
        var_4 = len(msg)
        
        # loop
        while (var_8 < len(msg)): # "i < len(msg)"
            var_A = var_A ^ msg[var_8] # xor-checksum calculation on the msg content, char by char, starts from msg[2] (bcs msg[0] = len, msg[1] = xor key)
            var_8 += 1 # "i++"
        
        if (var_A == var_9): # (xor calculation by the given xor key) == (msg[1], our xor-msg val)
            return True # valid
        
        return False # invalid

        raise NotImplementedError()


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msg-file>'.format(argv[0]))
        return -1
    path = argv[1]
    if check_message(path):
        print('valid message')
        return 0
    else:
        print('invalid message')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
