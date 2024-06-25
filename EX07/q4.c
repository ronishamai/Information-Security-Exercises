#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/user.h>

int pid = 0x12345678;

int main(int argc, char **argv) {
    // Make the malware stop waiting for our output by forking a child process:
    if (fork() != 0) {
        // Kill the parent process so we stop waiting from the malware
        return 0;
    } else {
        // Close the output stream so we stop waiting from the malware
        fclose(stdout);
    }

    // The rest of your code goes here
    
    if (ptrace(PTRACE_ATTACH, pid, NULL, NULL) == -1) {  // Attach to the process
      perror("attach");
      return 1;
    }
    
    int status;
    waitpid(pid, &status, 0);  // Wait for the process to stop
    if (WIFEXITED(status)) {
        return 1; 
    }  // Abort if the process exits


    while (!WIFEXITED(status)) {
        
        ptrace(PTRACE_SYSCALL, pid, NULL, NULL);

        struct user_regs_struct regs;
        ptrace(PTRACE_GETREGS, pid, NULL, &regs);  
        
        if (regs.orig_eax == 3) { // Read syscall: %eax = 3
            regs.edx = 0; // Read syscall: %edx = length (the return value), put 0 instead
            ptrace(PTRACE_SETREGS, pid, NULL, &regs);
        }    
    }
    
    if (ptrace(PTRACE_DETACH, pid, NULL, NULL) == -1) {  // Detach when done
      perror("detach");
      return 1;
    }
    
    return 0;
}
