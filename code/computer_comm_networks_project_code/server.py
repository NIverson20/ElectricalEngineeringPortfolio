import socket
import sys
import os

# command line arguments
SERVER_PORT = int(sys.argv[1])
PROTOCOL = sys.argv[2]

# import the correct transport protocol depending on user input
if PROTOCOL == "tcp":
    from tcp_transport import send_file
elif PROTOCOL == "snw":
    from snw_transport import (send_length, receive_length, send_data_chunk, receive_data_chunk,
                               send_file, receive_file)
else:
    print(f"Invalid Protocol {PROTOCOL}")
    sys.exit(1)

# 1000 Byte chunk size
CHUNK_SIZE = 1000

if __name__ == "__main__":

    if PROTOCOL == "tcp":
        # create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("", SERVER_PORT))
        server_socket.listen()

        while True:
            conn, addr = server_socket.accept()
            # get file name and command
            with conn:

                command = conn.recv(3)  # expecting "PUT" or "GET"

                if command == b"PUT":
                    filename = conn.recv(1024).decode().strip()  # get file name
                    conn.sendall(b"FILENAME RECEIVED")  # confirm file name

                    file_size = int(conn.recv(16).strip())  # get size of file
                    data = b""
                    # download the file
                    while len(data) < file_size:
                        packet = conn.recv(file_size - len(data))
                        if not packet:
                            break
                        data += packet

                    with open(filename, "wb") as f:
                        f.write(data)

                # get file name and send file
                elif command == b"GET":
                    filename = conn.recv(1024).decode().strip()
                    send_file(conn, filename)

    # snw put command
    elif PROTOCOL == "snw":
        # create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(("", SERVER_PORT))

        while True:
            command, addr = server_socket.recvfrom(1024)  # expecting "PUT" or "GET"

            if command == b"PUT":
                # get file length
                file_size = receive_length(server_socket)
                data_received = b""

                # get file in chunks
                while len(data_received) < file_size:
                    server_socket.settimeout(1)  # Timeout

                    try:
                        # get size left to be sent
                        remaining_size = file_size - len(data_received)
                        expected_chunk_size = min(CHUNK_SIZE, remaining_size)

                        # get the chunk
                        data_chunk = receive_data_chunk(server_socket, expected_chunk_size)
                        data_received += data_chunk

                        # send ACK
                        server_socket.sendto(b"ACK", addr)

                        # Timeout wait for ACK
                        server_socket.settimeout(1)

                    except socket.timeout:
                        # got all data
                        if len(data_received) == file_size:
                            break

                        # Timeout occurred
                        print("Data transmission terminated prematurely.")
                        sys.exit(1)

                # reset the timeout
                server_socket.settimeout(None)

                # get file name
                filename, _ = server_socket.recvfrom(1024)

                # save file to directory
                with open(filename.decode().strip(), "wb") as f:
                    f.write(data_received)

                # end FIN after getting all data
                server_socket.sendto(b"FIN", addr)

            # snw get command
            elif b"GET:" in command:
                # get file name from cache
                filename = command[4:].decode().strip()
                base_filename = os.path.basename(filename)

                # make sure server has file
                if not os.path.exists(filename):
                    print(f"File {filename} not found on the server.")
                    server_socket.sendto(b"FILE NOT FOUND", addr)
                    continue

                # send file size
                with open(filename, "rb") as file:
                    # Send the file size first
                    file_size = os.path.getsize(filename)
                    send_length(server_socket, addr, file_size)
                    sent_bytes = 0

                    while sent_bytes < file_size:
                        # get each data chunk
                        data_chunk = file.read(CHUNK_SIZE)

                        # send chunk to cache
                        send_data_chunk(server_socket, addr, data_chunk)
                        sent_bytes += len(data_chunk)

                        # wait for ACK
                        ack, _ = server_socket.recvfrom(3)
                        if ack != b"ACK":
                            print("Did not receive acknowledgment. Terminating.")
                            break

