#pragma once

#include <atomic>
#include <string>

#define DEFAULT_SEGMENT_SIZE (10 * 1024 * 1024)
#define NUM_READERS 10
#define ALIGN(n) ((n + (8 - 1)) & -8)

#define UNUSED(x) (void)x
#define UNPACK64(higher, lower, input) do {uint64_t tmp = input; higher = tmp >> 32; lower = tmp & 0xFFFFFFFF;} while (0)
#define PACK64(output, higher, lower) output = ((uint64_t)higher << 32) | ((uint64_t)lower & 0xFFFFFFFF)

struct  msgq_header_t {
  uint64_t num_readers;
  uint64_t write_pointer;
  uint64_t write_uid;
  uint64_t read_pointers[NUM_READERS];
  uint64_t read_valids[NUM_READERS];
  uint64_t read_uids[NUM_READERS];
};

struct msgq_queue_t {
  std::atomic<uint64_t> *num_readers;
  std::atomic<uint64_t> *write_pointer;
  std::atomic<uint64_t> *write_uid;
  std::atomic<uint64_t> *read_pointers[NUM_READERS];
  std::atomic<uint64_t> *read_valids[NUM_READERS];
  std::atomic<uint64_t> *read_uids[NUM_READERS];
  char * mmap_p;
  char * data;
  size_t size;
  int reader_id;
  uint64_t read_uid_local;
  uint64_t write_uid_local;

  bool read_conflate;
  std::string endpoint;
};

struct msgq_msg_t {
  size_t size;
  char * data;
};

void msgq_reset_reader(msgq_queue_t *q);
int msgq_msg_init_size(msgq_msg_t *msg, size_t size);
int msgq_msg_close(msgq_msg_t *msg);

int msgq_new_queue(msgq_queue_t * q, const char * path, size_t size);
void msgq_close_queue(msgq_queue_t *q);
void msgq_init_subscriber(msgq_queue_t * q);
void msgq_init_publisher(msgq_queue_t * q);

int msgq_msg_recv(msgq_msg_t *msg, msgq_queue_t *q);
int msgq_msg_send(msgq_msg_t *msg, msgq_queue_t *q);

bool msgq_all_readers_updated(msgq_queue_t *q);