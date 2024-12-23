#include <iostream>
#include "msgq.h"
#include "ipc.h"

int main()
{
    msgq_queue_t msg_queue;
    size_t size = 1024;
    const std::string shm_name = "/my_message";

    MSGQSubSocket *sub_socket = MSGQSubSocket::create(shm_name);

    std::cout << "Creates sub socket\n";

    MSGQMessage *msg = NULL;
    size_t msg_ctr = 0;

    while (msg_ctr <= 10) {
        msg = sub_socket->receive();
        if (msg != NULL) {
            std::cout << "Received message of size " << msg->getSize() << " bytes: " << msg->getData() << std::endl;
            msg_ctr++;
        }
    }

    std::cout << "Closing subscriber socket." << std::endl;

    delete sub_socket;

    return 0;
}