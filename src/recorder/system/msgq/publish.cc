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

    // create message queue
    int res = msgq_new_queue(&msg_queue, shm_name.c_str(), size);
    if (res != 0)
    {
        std::cout << "Could not create shared memory message queue." << std::endl;
        return -1;
    }

    std::cout << "Message queue created successfully." << std::endl;

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