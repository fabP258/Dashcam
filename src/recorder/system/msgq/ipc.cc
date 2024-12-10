#include <cstring>
#include <iostream>
#include "ipc.h"
#include "msgq.h"


void MSGQMessage::init(size_t size) {
  m_data = new char[size];
}

void MSGQMessage::init(char * d, size_t size) {
  m_data = new char[size];
  memcpy(m_data, d, size);
}

void MSGQMessage::takeOwnership(char * data, size_t size) {
  m_size = size;
  m_data = data;
}

void MSGQMessage::close() {
  if (m_size > 0){
    delete[] m_data;
  }
  m_size = 0;
}

MSGQMessage::~MSGQMessage() {
  this->close();
}

MSGQSubSocket::~MSGQSubSocket(){
  if (m_q != NULL){
    msgq_close_queue(m_q);
    delete m_q;
  }
}

MSGQSubSocket * MSGQSubSocket::create(std::string endpoint, bool conflate){
  MSGQSubSocket *s = new MSGQSubSocket();
  int r = s->connect(endpoint, conflate);

  if (r == 0) {
    return s;
  }

  std::cerr << "Error, failed to connect SubSocket to " << endpoint << ": " << strerror(errno) << std::endl;

  delete s;
  return nullptr;
}

int MSGQSubSocket::connect(std::string endpoint, bool conflate){
  m_q = new msgq_queue_t;
  int r = msgq_new_queue(m_q, endpoint.c_str(), DEFAULT_SEGMENT_SIZE);
  if (r != 0){
    return r;
  }

  msgq_init_subscriber(m_q);

  if (conflate){
    m_q->read_conflate = true;
  }

  return 0;
}

MSGQMessage * MSGQSubSocket::receive(){
  // NOTE: Only non-blocking receive implemented so far

  msgq_msg_t msg;
  int rc = msgq_msg_recv(&msg, m_q);

  MSGQMessage *r = NULL;
  if (rc > 0) {
    r = new MSGQMessage;
    r->takeOwnership(msg.data, msg.size);
  } else {
    msgq_msg_close(&msg);
  }

  return r;
}

MSGQPubSocket * MSGQPubSocket::create(std::string endpoint){
  MSGQPubSocket * s = new MSGQPubSocket();
  int r = s->connect(endpoint);

  if (r == 0) {
    return s;
  }
   
  std::cerr << "Error, failed to bind MSGQPubSocket to " << endpoint << ": " << strerror(errno) << std::endl;

  delete s;
  return nullptr;
}

int MSGQPubSocket::connect(std::string endpoint){
  m_q = new msgq_queue_t;
  int r = msgq_new_queue(m_q, endpoint.c_str(), DEFAULT_SEGMENT_SIZE);
  if (r != 0)
  {
    return r;
  }

  msgq_init_publisher(m_q);

  return 0;
}

int MSGQPubSocket::send(MSGQMessage *message){
  msgq_msg_t msg;
  msg.data = message->getData();
  msg.size = message->getSize();

  return msgq_msg_send(&msg, m_q);
}

int MSGQPubSocket::send(char *data, size_t size){
  msgq_msg_t msg;
  msg.data = data;
  msg.size = size;

  return msgq_msg_send(&msg, m_q);
}

bool MSGQPubSocket::all_readers_updated(){
  return msgq_all_readers_updated(m_q);
}

MSGQPubSocket::~MSGQPubSocket(){
  if (m_q != NULL) {
    msgq_close_queue(m_q);
    delete m_q;
  }
}