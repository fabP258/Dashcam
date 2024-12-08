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

class MSGQSubSocket {
private:
  msgq_queue_t * m_q = NULL;
public:
  ~MSGQSubSocket();
  static MSGQSubSocket * create(std::string endpoint, bool conflate=false);
  int connect(std::string endpoint, bool conflate=false);
  void * getRawSocket() {return (void*)m_q;}
  MSGQMessage *receive();
};

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