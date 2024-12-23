import time
from ipc_pyx import PubSocket

pub_socket = PubSocket(b"/my_message")
msg = "Hello World!"

for i in range(100):
    print(f"Sending message {i}")
    pub_socket.send(msg.encode("utf-8"))
    time.sleep(1)

print(f"Finished sending messages.")
