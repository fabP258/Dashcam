#include <iostream>
#include <cstring>
#include <thread>
#include <chrono>
#include "msgq.h"
#include "ipc.h"

int main()
{
    msgq_queue_t msg_queue;
    size_t size = 1024;
    const std::string shm_name = "/my_message";

    MSGQPubSocket *pub_socket = MSGQPubSocket::create(shm_name);

    std::cout << "Created pub socket\n";

    char *msg = "New Message";
    size_t msg_size = strlen(msg);

    size_t i = 0;
    while (i < 100) {
      std::cout << "Sending message " << i << std::endl;
      pub_socket->send(msg, msg_size);
      std::this_thread::sleep_for(std::chrono::seconds(1));
      i++;
    }

    delete pub_socket;

    return 0;
}