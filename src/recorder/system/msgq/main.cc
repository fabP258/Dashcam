#include <iostream>
#include <sys/mman.h>
#include "msgq.h"
#include "ipc.h"
#include "imu.h"

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

    imu_message_t imu_msg = {0.6f, 1.1f, 9.2f};
    size_t msg_size = sizeof(imu_message_t);

    pub_socket->send(reinterpret_cast<char*>(&imu_msg), msg_size);

    // TODO: check if write pointer increased, etc. ... 

    delete pub_socket;

    return 0;
}