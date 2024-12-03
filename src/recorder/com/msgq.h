#pragma once

#include <atomic>
#include <string>

#define NUM_READERS 10

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

int msgq_new_queue(msgq_queue_t * q, const char * path, size_t size);
void msgq_close_queue(msgq_queue_t *q);