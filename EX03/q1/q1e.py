def patch_program_data(program: bytes) -> bytes:
    """
    Implement this function to return the patched program. This program should
    return 0 for all input files.

    The fix in this file should be *different* than the fix in q1d.py.

    :param data: The bytes of the source program.
    :return: The bytes of the patched program.
    """
    # the offset of the test instruction after validate call
    mov_offset = 0x6DD
    
    # 0xB8 for mov (op-code)
    # 0x00,0x00,0x00,0x00 for 0 const
    mov_0_inst =  bytes([0xB8,0x00,0x00,0x00,0x00]) 

    # changing the instructions in the program
    patched = program[:mov_offset] + mov_0_inst + program[mov_offset+5:]
    
    # nop's s.t. |program| = |patched|
    patched += b'\x90' * (len(program) - len(patched))
    
    # return patched program
    return patched
    
    raise NotImplementedError()


def patch_program(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    patched = patch_program_data(data)
    with open(path + '.patched', 'wb') as writer:
        writer.write(patched)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msgcheck-program>'.format(argv[0]))
        return -1
    path = argv[1]
    patch_program(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
