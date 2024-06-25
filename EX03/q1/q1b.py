def fix_message_data(data: bytes) -> bytes:
    """
    Implement this function to return the "fixed" message content. This message
    should have minimal differences from the original message, but should pass
    the check of `msgcheck`.

    :param data: The source message data.
    :return: The fixed message data.
    """

    # init args
    arg_0 = data[0] # msg len
    var_4 = arg_0 
    var_9 = data[1] # xor msg val
    var_A = 0x19 # xor key
    var_8 = 2 # loop variable (over the msg)
        
    data = data[:2+arg_0]
    var_4 = len(data)
        
    # loop
    while (var_8 < len(data)): # "i < len(msg)"
        var_A = var_A ^ data[var_8] # xor-checksum calculation on the msg content, char by char, starts from msg[2] (bcs msg[0] = len, msg[1] = xor key)
        var_8 += 1 # "i++"
        
    if (var_A == var_9): # (xor calculation by the given xor key) == (msg[1], our xor-msg val)
        return data # valid
        
    else: # xor calculation by the given xor key != msg[1], xor-msg val -> invalid -> fix
        data = bytearray(data)
        data[1] = var_A # change the xor msg val to be the xor-value we calculated by the given xor key
        return bytes(data) # return the fixed msg
    
    raise NotImplementedError()


def fix_message(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    fixed_data = fix_message_data(data)
    with open(path + '.fixed', 'wb') as writer:
        writer.write(fixed_data)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msg-file>'.format(argv[0]))
        return -1
    path = argv[1]
    fix_message(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
