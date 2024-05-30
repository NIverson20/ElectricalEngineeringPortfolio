import socket
import os
import sys

# command line arguments
CACHE_SERVER_PORT = int(sys.argv[1])
SERVER_IP = sys.argv[2]
SERVER_PORT = int(sys.argv[3])
PROTOCOL = sys.argv[4]

# 1000 Byte chunk size
CHUNK_SIZE = 1000

# import the correct transport protocol depending on user input
if PROTOCOL == "tcp":
    from tcp_transport import forward_request_to_server
elif PROTOCOL == "snw":
    from snw_transport import (send_length, receive_length, send_data_chunk, receive_data_chunk,
                               send_file, receive_file)
else:
    print(f"Invalid Protocol {PROTOCOL}")
    sys.exit(1)

if __name__ == "__main__":

    if PROTOCOL == "tcp":
        # using tcp transport open new socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cache_server_socket:
            # bind to server
            cache_server_socket.bind(("", CACHE_SERVER_PORT))
            cache_server_socket.listen()

            while True:
                # get file name from client
                conn, addr = cache_server_socket.accept()
                with conn:
                    filename = conn.recv(1024).decode().strip()
                    base_filename = os.path.basename(filename)  # get just the filename from path

                    if os.path.exists(base_filename):  # if cache has path send to client
                        with open(base_filename, "rb") as f:
                            data = f.read()
                            conn.sendall(b"cache ")
                    else:
                        # if file not on cache get from server
                        data = forward_request_to_server(filename, SERVER_IP, SERVER_PORT)
                        if data:
                            # put the file to in caches directory
                            with open(base_filename, "wb") as f:
                                f.write(data)
                            conn.sendall(b"origin")

                    # check to make sure there is data in the file
                    if data:
                        conn.sendall(f"{len(data):<16}".encode())
                        conn.sendall(data)
                    else:
                        conn.sendall(b"0000000000000000")

    # snw get command
    elif PROTOCOL == "snw":
        # create socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cache_server_socket:
            cache_server_socket.bind(("", CACHE_SERVER_PORT))

            while True:
                message, client_address = cache_server_socket.recvfrom(1024)

                # make sure the get command was sent
                if message.startswith(b"GET:"):
                    # get just the file name
                    filename = message[4:].decode().strip()
                    base_filename = os.path.basename(filename)

                    if os.path.exists(base_filename):  # check if the cache has the file
                        cache_server_socket.sendto(b"FROM:CACHE", client_address)

                        # open the file on the cache
                        with open(base_filename, "rb") as f:
                            file_data = f.read()

                            # send the file length to the client
                            if not send_length(cache_server_socket, client_address, len(file_data)):
                                print("Error sending file length.")
                                continue

                            # send file in chucks
                            for i in range(0, len(file_data), CHUNK_SIZE):
                                data_chunk = file_data[i:i + CHUNK_SIZE]
                                if not send_data_chunk(cache_server_socket, client_address, data_chunk):
                                    print(f"Error sending chunk {i // CHUNK_SIZE + 1}.")
                                    break
                    else:
                        # cache doesnt have file
                        cache_server_socket.sendto(b"FROM:ORIGIN", client_address)

                        # create socket
                        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
                            server_socket.settimeout(10)  # Timeout

                            # send the server the get command and file name
                            get_msg = f"GET:{filename}".encode()
                            server_socket.sendto(get_msg, (SERVER_IP, SERVER_PORT))

                            # get the file length from the server
                            file_length = receive_length(server_socket)
                            if file_length is None:
                                print("Error receiving file length.")
                                continue

                            # download the file to the cache
                            received_bytes = 0
                            file_data = b""
                            while received_bytes < file_length:
                                data_chunk = receive_data_chunk(server_socket)
                                if not data_chunk:
                                    print("Error receiving chunk of data.")
                                    break
                                received_bytes += len(data_chunk)
                                file_data += data_chunk
                                server_socket.sendto(b"ACK", (SERVER_IP, SERVER_PORT))  # send ACK after each chunk

                            # save to cache directory
                            with open(base_filename, "wb") as f:
                                f.write(file_data)

                            # send the data to the client
                            if os.path.exists(base_filename):  # cmake sure cache has file
                                with open(base_filename, "rb") as f:
                                    file_data = f.read()

                                    # send file length to client
                                    if not send_length(cache_server_socket, client_address, len(file_data)):
                                        print("Error sending file length.")
                                        continue

                                    # send each chunk to client
                                    for i in range(0, len(file_data), CHUNK_SIZE):
                                        data_chunk = file_data[i:i + CHUNK_SIZE]
                                        if not send_data_chunk(cache_server_socket, client_address, data_chunk):
                                            print(f"Error sending chunk {i // CHUNK_SIZE + 1}.")
                                            break







