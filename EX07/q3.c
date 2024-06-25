#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int pid = 0x12345678;
int addr_check_if_virus = 0x12341234;
int addr_check_if_virus_alternative = 0x12123434;

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

    
    // PTRACE_POKEDATA copy the word data to the address addr in the tracees memory.
    if (ptrace(PTRACE_POKEDATA, pid, addr_check_if_virus, addr_check_if_virus_alternative) == -1) {
        perror("pokedata");
        return 1;
    }
    
    
    
    if (ptrace(PTRACE_DETACH, pid, NULL, NULL) == -1) {  // Detach when done
      perror("detach");
      return 1;
    }

    return 0;
}
