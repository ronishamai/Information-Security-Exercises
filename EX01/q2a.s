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
    
    stop_conditions:
        cmp ebx,0 # compare n to 0
        jle return_zero # if the integer is equal/less than 0, the result should be 0
        
        cmp ebx,1 # compare n to 1
        je return_one # if the integer is 1, the result should be 1
       
        jmp calculate_sqaurebonacci # if n is greater than 1, return (a_n-1)^2+(a_n-2)^2
    
    return_zero:
        xor eax,eax # save 0 in the register eax
	    jmp end   
     
    return_one:
        mov eax,1 # save 1 in the register eax  
        jmp end   

    calculate_sqaurebonacci:  
        
        # push n-1 to stack -> caclulate sqaurebonacci(n-1) by recursion -> calculate (a_n-1)^2 -> pop n-1 from the stack -> push (a_n-1)^2 to the stack
                  
        sub eax,1 # calculate n-1
        push eax # push n-1 to stack
        call my_function # caclulate sqaurebonacci(n-1) by recursion
        mul eax # calculate (a_n-1)^2
        mov ebx,eax # save eax in ebx (tmp var)
        pop eax # pop n-1 from the stack
        push ebx # push (a_n-1)^2 to the stack
        
        # push n-2 to stack -> caclulate sqaurebonacci(n-2) by recursion -> clean up stack after our call -> restore (a_n-1)^2 from stack -> calculate (a_n-2)^2 
        
        sub eax,1 # calculate n-2 
        push eax # push n-2 to stack
        call my_function  # caclulate sqaurebonacci(n-2) by recursion
        add esp,4 # clean up stack after our call
        pop ebx # restore (a_n-1)^2 from stack
        mul eax # calculate (a_n-2)^2
        
        # calculate sqaurebonacci(n): a_n = (a_n-1)^2+(a_n-2)^2
        
        add eax,ebx # sqaurebonacci definition: a_n = (a_n-1)^2+(a_n-2)^2

    end:
        mov esp,ebp # restore the initial value of esp from ebp
    	pop ebp # restore at the end ("epilogue")
        ret # pop eip & jumps back to the ra
