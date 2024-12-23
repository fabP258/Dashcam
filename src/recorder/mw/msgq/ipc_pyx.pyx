from libcpp.string cimport string
from libcpp cimport bool

cdef extern from "ipc.h":
  cdef cppclass MSGQMessage:
    void init(size_t)
    void init(char *, size_t)
    void close()
    size_t getSize()
    char *getData()

  cdef cppclass MSGQSubSocket:
    @staticmethod
    MSGQSubSocket * create(string, bool)
    MSGQMessage * receive()
  
  cdef cppclass MSGQPubSocket:
    @staticmethod
    MSGQPubSocket * create(string)
    int send (char *, size_t)

cdef class SubSocket:
  cdef MSGQSubSocket * socket

  def __cinit__(self, string endpoint, bool conflate=False):
    self.socket = MSGQSubSocket.create(endpoint, conflate)

    if self.socket == NULL:
      raise Exception("Failed to create cppSubSocket.")

  def __dealloc__(self):
    if self.socket != NULL:
      del self.socket

  def receive(self):
    msg = self.socket.receive()

    if msg == NULL:
      return None
    else:
      sz = msg.getSize()
      data = msg.getData()[:sz]
      del msg

      return data

cdef class PubSocket:
  cdef MSGQPubSocket * socket

  def __cinit__(self, string endpoint):
    self.socket = MSGQPubSocket.create(endpoint)
    if self.socket == NULL:
      raise Exception("Failed to create cppPubSocket.")

  def __dealloc__(self):
    if self.socket != NULL:
      del self.socket

  def send(self, bytes data):
    length = len(data)
    r = self.socket.send(<char*>data, length)

    if r != length:
      raise Exception("Failed to sen message")