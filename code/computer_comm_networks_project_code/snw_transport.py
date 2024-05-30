import socket

# size of chunk
CHUNK_SIZE = 1000


# send the length
def send_length(client_socket, server_address, length):
    length_message = f"LEN:{length}".encode()  # send the length with the LEN identifier
    try:
        client_socket.sendto(length_message, server_address)
        ack, _ = client_socket.recvfrom(3)  # get ACK
        if ack == b"ACK":
            return True
    except socket.timeout:
        print("Timeout while waiting for acknowledgment.")
    return False


# get the file length and send the int length and send ACK
def receive_length(receiver_socket):

    length_msg, sender_addr = receiver_socket.recvfrom(1024)
    if length_msg.startswith(b"LEN:"):
        receiver_socket.sendto(b"ACK", sender_addr)
        return int(length_msg.split(b":")[1])

    return None


def send_data_chunk(sock, addr, data_chunk):
    # send a chunk of data and wait for ACK before sending another
    sock.sendto(data_chunk, addr)
    try:
        ack_message, _ = sock.recvfrom(3)  # wait for ACK
        if ack_message == b"ACK":
            return True
    except socket.timeout:
        print("Timeout while waiting for acknowledgment.")
    return False


# get the file chunk on at a time and take into account for last chunk which is smaller than 1000 Bytes
def receive_data_chunk(sock, expected_size=None):

    if not expected_size:
        expected_size = CHUNK_SIZE
    data_chunk, addr = sock.recvfrom(expected_size)
    sock.sendto(b"ACK", addr)  # send ACK
    return data_chunk


# send file in the chunks
def send_file(sock, addr, filepath):
    with open(filepath, "rb") as f:
        file_data = f.read()
        send_length(sock, addr, len(file_data))  # send the length
        for i in range(0, len(file_data), CHUNK_SIZE):  # sent the file in chunks
            data_chunk = file_data[i:i+CHUNK_SIZE]
            while not send_data_chunk(sock, addr, data_chunk):
                pass


def receive_file(sock, save_as):
    total_length = receive_length(sock)  # download the length
    data_received = b""
    while len(data_received) < total_length:  # download the file for each chunk
        data_chunk = receive_data_chunk(sock)
        data_received += data_chunk  # combine the chunks together

    # save the file to directory
    with open(save_as, "wb") as f:
        f.write(data_received)
