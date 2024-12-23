from ipc_pyx import SubSocket

sub_socket = SubSocket(b"/my_message")

msg_ctr = 0

while msg_ctr <= 10:
    byte_data = sub_socket.receive()

    if byte_data is not None:
        string_data = byte_data.decode("utf-8")
        print(f"Receive message {msg_ctr}: {string_data}")
        msg_ctr += 1

print("Shutting down subscriber.")
