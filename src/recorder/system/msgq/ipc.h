#pragma once

#include <string>
#include "msgq.h"

class MSGQMessage{
private:
  char * m_data;
  size_t m_size;
public:
  void init(size_t size);
  void init(char *data, size_t size);
  void takeOwnership(char *data, size_t size);
  size_t getSize(){return m_size;}
  char * getData(){return m_data;}
  void close();
  ~MSGQMessage();
};

/*
class MSGQSubSocket {
private:
  msgq_queue_t * m_q = NULL;
  // TODO: is timeout needed for shared memory?
  int m_timeout;
public:
  int connect(std::string endpoint, bool conflate=false);
  void setTimeout(int timeout);
  void * getRawSocket() {return (void*)m_q;}
  static MSGQSubSocket * create(std::string endpoint, bool conflate=false);
  MSGQMessage *receive(bool non_blocking=false);
  ~MSGQSubSocket();
};
*/

class MSGQPubSocket {
private:
  msgq_queue_t * m_q = NULL;
public:
  ~MSGQPubSocket();
  static MSGQPubSocket * create(std::string endpoint);
  int connect(std::string endpoint);
  int send(MSGQMessage *message);
  int send(char *data, size_t size);
  bool all_readers_updated();
};