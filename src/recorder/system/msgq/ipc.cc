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
/*
MSGQSubSocket * MSGQSubSocket::create(std::string endpoint, bool conflate){
  MSGQSubSocket *s = new MSGQSubSocket();
  int r = s->connect(endpoint, conflate);

  if (r == 0) {
    return s;
  } else {
    std::cerr << "Error, failed to connect SubSocket to " << endpoint << ": " << strerror(errno) << std::endl;

    delete s;
    return nullptr;
  }
}

int MSGQSubSocket::connect(std::string endpoint, bool conflate){
  m_q = new msgq_queue_t;
  int r = msgq_new_queue(m_q, endpoint.c_str(), DEFAULT_SEGMENT_SIZE);
  if (r != 0){
    return r;
  }

  msgq_init_subscriber(q);

  if (conflate){
    q->read_conflate = true;
  }

  m_timeout = -1;

  return 0;
}

MSGQMessage * MSGQSubSocket::receive(bool non_blocking){
  msgq_do_exit = 0;

  // TODO: do we need support for polling?

  void (*prev_handler_sigint)(int);
  void (*prev_handler_sigterm)(int);
  if (!non_blocking){
    prev_handler_sigint = std::signal(SIGINT, sig_handler);
    prev_handler_sigterm = std::signal(SIGTERM, sig_handler);
  }

  msgq_msg_t msg;

  MSGQMessage *r = NULL;

  int rc = msgq_msg_recv(&msg, q);

  // Hack to implement blocking read with a poller. Don't use this
  while (!non_blocking && rc == 0 && msgq_do_exit == 0){
    msgq_pollitem_t items[1];
    items[0].q = q;

    int t = (m_timeout != -1) ? m_timeout : 100;

    int n = msgq_poll(items, 1, t);
    rc = msgq_msg_recv(&msg, q);

    // The poll indicated a message was ready, but the receive failed. Try again
    if (n == 1 && rc == 0){
      continue;
    }

    if (m_timeout != -1){
      break;
    }
  }


  if (!non_blocking){
    std::signal(SIGINT, prev_handler_sigint);
    std::signal(SIGTERM, prev_handler_sigterm);
  }

  errno = msgq_do_exit ? EINTR : 0;

  if (rc > 0){
    if (msgq_do_exit){
      msgq_msg_close(&msg); // Free unused message on exit
    } else {
      r = new MSGQMessage;
      r->takeOwnership(msg.data, msg.size);
    }
  }

  return (Message*)r;
}
*/

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