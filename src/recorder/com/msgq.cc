#include <iostream>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

#include "msgq.h"

int msgq_new_queue(msgq_queue_t * q, const char * path, size_t size)
{
    // create shared memory object file
    int shm_fd = shm_open(path, O_CREAT | O_RDWR, 0666);
    if (shm_fd < 0)
    {
        std::cout << "Warning: Could not create shared memory object." << std::endl;
        return -1;
    }

    // truncates file to size
    if (ftruncate(shm_fd, size + sizeof(msgq_header_t)) == -1)
    {
        close(shm_fd);
        return -1;
    }

    // map shared memory into proc adress space
    void* shm_ptr = mmap(NULL, size + sizeof(msgq_header_t), PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (shm_ptr == MAP_FAILED)
    {
        close(shm_fd);
        return -1;
    }
    close(shm_fd);

    char *buffer = static_cast<char *>(shm_ptr);

    // fill queue struct
    q->mmap_p = buffer;

    msgq_header_t *header = (msgq_header_t *)buffer;

    // Setup pointers to header segment
    q->num_readers = reinterpret_cast<std::atomic<uint64_t>*>(&header->num_readers);
    q->write_pointer = reinterpret_cast<std::atomic<uint64_t>*>(&header->write_pointer);
    q->write_uid = reinterpret_cast<std::atomic<uint64_t>*>(&header->write_uid);

    for (size_t i = 0; i < NUM_READERS; i++){
        q->read_pointers[i] = reinterpret_cast<std::atomic<uint64_t>*>(&header->read_pointers[i]);
        q->read_valids[i] = reinterpret_cast<std::atomic<uint64_t>*>(&header->read_valids[i]);
        q->read_uids[i] = reinterpret_cast<std::atomic<uint64_t>*>(&header->read_uids[i]);
    }

    q->data = buffer + sizeof(msgq_header_t);
    q->size = size;
    q->reader_id = -1;

    q->endpoint = path;
    q->read_conflate = false;

    return 0;
}

void msgq_close_queue(msgq_queue_t *q){
  if (q->mmap_p != NULL){
    munmap(q->mmap_p, q->size + sizeof(msgq_header_t));
  }
}