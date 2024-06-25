from infosec.core import assemble


def patch_program_data(program: bytes) -> bytes:
    """
    Implement this function to return the patched program. This program should
    execute lines starting with #!, and print all other lines as-is.

    Use the `assemble` module to translate assembly to bytes. For help, in the
    command line run:

        ipython3 -c 'from infosec.core import assemble; help(assemble)'

    :param data: The bytes of the source program.
    :return: The bytes of the patched program.
    """
    program = bytearray(program)
    
    p1 = assemble.assemble_file("patch1.asm")
    for i in range(len(p1)):
        program[0x633 + i] = p1[i] # 0x633 = start offset of small deadzone
        
    p2 = assemble.assemble_file("patch2.asm")
    for i in range(len(p2)):
        program[0x5CD + i] = p2[i] # 0x5CD = start offset of big deadzone
    return program


def patch_program(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    patched = patch_program_data(data)
    with open(path + '.patched', 'wb') as writer:
        writer.write(patched)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <readfile-program>'.format(argv[0]))
        return -1
    path = argv[1]
    patch_program(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
