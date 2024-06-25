#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int pid = 0x12345678;
int addr = 0x12341234;

int main() {

    if (ptrace(PTRACE_ATTACH, pid, NULL, NULL) == -1) {  // Attach to the process
      perror("attach");
      return 1;
    }
    
    int status;
    waitpid(pid, &status, 0);  // Wait for the process to stop
    if (WIFEXITED(status)) { 
        return 1; 
    }  // Abort if the process exits
    
    

    // PTRACE_POKEDATA copy the word data to the address addr in the tracees memory
    int xor_eax_eax_ret_nop = 0xc3c03190;
    if (ptrace(PTRACE_POKEDATA, pid, addr, xor_eax_eax_ret_nop) == -1) {
        perror("pokedata");
        return 1;
    }
    
    
    
    if (ptrace(PTRACE_DETACH, pid, NULL, NULL) == -1) {  // Detach when done
      perror("detach");
      return 1;
    }

    return 0;
}

