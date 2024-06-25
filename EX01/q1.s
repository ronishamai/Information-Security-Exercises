# Declare the assembly flavor to use the intel syntax.
.intel_syntax noprefix

# Define a symbol to be exported from this file.
.global my_function

# Declare symbol type to be a function.
.type my_function, @function

# Code follows below.

my_function:
    
    # credid: wikipedia, algorithm using linear search
    # pseudo code: isqrt(y) {l = 0; while ((l+1)(l+1)<=y) {l+=1;} return l;} 
    # eax:=tmp, ebx:=y, ecx:=l
     
    mov ebx, dword ptr [esp+4] # read the input to the function from ebx (init y)
    push ebp # save the beginning ("prologue")
    mov ebp,esp # save the initial value of esp in ebp
    
    cmp ebx,1 # compare input to 1
    jl return_zero # return zero if input is less than 1
    
    xor ecx,ecx # l = 0
    
    while:
        inc ecx # l = l + 1
	    mov eax,ecx # tmp = l + 1
        mul ecx # tmp = tmp * (l + 1) = (l + 1) * (l + 1)
        cmp eax,ebx # compare (l+1) * (l+1) to y
        
        je return_sqrt # jump to return_sqrt label if (l+1) * (l+1) = y, found integer sqrt(y)
        jg return_zero # jump to return_zero label if (l+1) * (l+1) > y, there is no integer sqrt(y)
        
        jmp while 
    
    return_zero:
        xor eax,eax # eax = zero, save the result in the register eax
	    jmp end   
     
    return_sqrt:
        mov eax,ecx # save the result in the register eax  
    
    end:
    	mov esp,ebp # restore the initial value of esp from ebp
    	pop ebp # restore at the end ("epilogue")
    
    ret # pop eip & jumps back to the ra
     

