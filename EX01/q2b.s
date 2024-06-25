# Declare the assembly flavor to use the intel syntax.
.intel_syntax noprefix

# Define a symbol to be exported from this file.
.global my_function

# Declare symbol type to be a function.
.type my_function, @function

# Code follows below.

my_function:
    
    mov ebx, dword ptr [esp+4] # read the input to the function from ebx (init n) 
    push ebp # save the beginning ("prologue")
    mov ebp,esp # save the initial value of esp in ebp
    
    cmp ebx,0 # compare n to 0
    jle return_zero # if the integer is equal/less than 0, the result should be 0
        
    cmp ebx,1 # compare n to 1
    je return_one # if the integer is 1, the result should be 1
    
    mov ecx,0 # init a0 = 0
    mov eax,1 # init a1 = 1
    
    for:
    
        # calculate n-2 squarebonacci numbers (a0,a1 already given) iteratively
        cmp ebx,1
        jbe end
        
        # a series of actions, starts with: eax:= a_n-1, ecx:=a_n-2, ends with: eax:= a_n, ecx:=a_n-1:
        push eax # stack <- a_n-1
        mul eax # ecx <- (a_n-1)^2
        push eax # stack <- (a_n-1)^2
  
        mov eax,ecx
        mul ecx # eax <- (a_n-2)^2
        
        pop ecx # ecx <- (a_n-1)^2
        add eax,ecx # eax <- a_n = (a_n-1)^2 + (a_n-2)^2
        pop ecx # ecx <- a_n-1
        
        dec ebx # n-=1
        jmp for # loop

    jmp end # eax:= a_n, return its value

    return_zero:
        mov eax,0 # save 0 in the register eax
	    jmp end   
     
    return_one:
        mov eax,1 # save 1 in the register eax  
        jmp end  
    
    end:    
        mov esp,ebp # restore the initial value of esp from ebp
        pop ebp # restore at the end ("epilogue")
        ret # pop eip & jumps back to the ra
