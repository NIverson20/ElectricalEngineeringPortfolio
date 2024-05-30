import socket
import sys
import os

# command line arguments
SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
CACHE_SERVER_IP = sys.argv[3]
CACHE_SERVER_PORT = int(sys.argv[4])
PROTOCOL = sys.argv[5]

# import the correct transport protocol depending on user input
if PROTOCOL == "tcp":
    from tcp_transport import receive_file_from_server, send_file_to_server
elif PROTOCOL == "snw":
    from snw_transport import (send_length, receive_length, send_data_chunk, receive_data_chunk,
                               send_file, receive_file)
else:
    print(f"Invalid Protocol {PROTOCOL}")
    sys.exit(1)

# 1000 Byte chunk size
CHUNK_SIZE = 1000

if __name__ == "__main__":

    while True:
        command = input("Enter Command: ")

        if command == "quit":
            print("Exiting program!")
            sys.exit(0)

        elif command.startswith("get "):
            print("Awaiting server response")

            # get file name from command line
            command_filename = command.split(" ")[1]
            # remove < > if in command
            command_filename = command_filename.replace('<', '').replace('>', '').strip()
            # get base filename with command
            base_filename = os.path.basename(command_filename)
            # remove < > if in command
            base_filename = base_filename.replace('<', '').replace('>', '').strip()

            # start tcp transport
            if PROTOCOL == "tcp":
                # init new socket and connect to cache server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cache_client:
                    cache_client.connect((CACHE_SERVER_IP, CACHE_SERVER_PORT))

                    cache_client.sendall(command_filename.encode())  # send file name to cache

                    source, data = receive_file_from_server(cache_client)  # receive file from either server or cache

                    with open(base_filename, "wb") as f:  # save file to client directory
                        f.write(data)

                        # print where the file came from
                        if source == "cache ":
                            print("Server response: File delivered from cache")
                        elif source == "origin":
                            print("Server response: File delivered from origin")

                    if not data:
                        print("Error File not delivered correctly")

            # start get command using snw transport
            elif PROTOCOL == "snw":
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cache_client:  # create new socket
                    cache_client.settimeout(10)  # timeout

                    # send the get command and file name to cache
                    get_msg = f"GET:{command_filename}".encode()
                    cache_client.sendto(get_msg, (CACHE_SERVER_IP, CACHE_SERVER_PORT))

                    # determine where file came from, print later if file downloaded
                    source_msg, _ = cache_client.recvfrom(1024)
                    if source_msg == b"FROM:CACHE":
                        file_from = 1
                    elif source_msg == b"FROM:ORIGIN":
                        file_from = 2
                    else:
                        print("Error: Unexpected source message.")
                        continue

                    # get file length from cache
                    file_length = receive_length(cache_client)
                    if file_length is None:
                        print("Error receiving file length.")
                        continue

                    cache_client.settimeout(1)  # Timeout

                    received_bytes = 0  # init bytes to 0
                    file_data = b""
                    try:
                        # get chunks unit all chunks received
                        while received_bytes < file_length:
                            data_chunk = receive_data_chunk(cache_client)
                            if not data_chunk:
                                print("Error receiving chunk of data.")
                                break
                            received_bytes += len(data_chunk)
                            file_data += data_chunk
                            cache_client.sendto(b"ACK", (CACHE_SERVER_IP, CACHE_SERVER_PORT))  # send ACK to cache
                    except socket.timeout:
                        print("Did not receive data. Terminating.")
                        sys.exit(1)

                    # download the file to directory
                    with open(base_filename, "wb") as f:
                        f.write(file_data)

                    # print the file location (where it came from)
                    if file_from == 1:
                        print("Server response: File delivered from cache.")
                    elif file_from == 2:
                        print("Server response: File delivered from origin server.")

        # start the put command
        elif command.startswith("put "):
            print("Awaiting server response")
            filepath = command.split(" ")[1]  # get filepath or name if in current directory
            filepath = filepath.replace('<', '').replace('>', '').strip()

            # if there is a file get data
            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    file_data = f.read()

                # start the tcp transport
                if PROTOCOL == "tcp":
                    # create new socket
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_client:
                        server_client.connect((SERVER_IP, SERVER_PORT))  # connect to server
                        if send_file_to_server(server_client, filepath):
                            print("Server response: File successfully uploaded")
                        else:
                            print("Error 15")

                # put using snw transport
                elif PROTOCOL == "snw":
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_client:
                        server_client.settimeout(10)  # Timeout

                        # send the server the put command
                        server_client.sendto(b"PUT", (SERVER_IP, SERVER_PORT))

                        # load the file data
                        with open(filepath, 'rb') as f:
                            file_data = f.read()

                        # send the length of the file
                        if not send_length(server_client, (SERVER_IP, SERVER_PORT), len(file_data)):
                            print("Error sending file length")
                            break

                        # send the file in chuck
                        for i in range(0, len(file_data), CHUNK_SIZE):
                            data_chunk = file_data[i:i + CHUNK_SIZE]
                            server_client.settimeout(1)  # Set timeout for 1 seconded if ACK no received

                            sent = send_data_chunk(server_client, (SERVER_IP, SERVER_PORT), data_chunk)
                            if not sent:
                                print("Did not receive ACK Terminating.")

                        # error handling for the last ACK
                        try:
                            response, _ = server_client.recvfrom(3)
                            if response != b"ACK":
                                print("Unexpected response after last chunk. Terminating")
                                sys.exit(1)
                        except socket.timeout:
                            print("Did not receive ACK for last chunk. Terminating")
                            sys.exit(1)

                        # clear out the socket to be able to receive the FIN statement
                        while True:
                            try:
                                leftover_msg, _ = server_client.recvfrom(3, socket.MSG_DONTWAIT)
                            except:
                                break

                        # send the filename after all chunks are sent
                        base_filename = os.path.basename(filepath)
                        server_client.sendto(base_filename.encode(), (SERVER_IP, SERVER_PORT))

                        # after getting FIN print file uploaded
                        response, _ = server_client.recvfrom(3)
                        if response == b"FIN":
                            print("Server response: File successfully uploaded.")
                        else:
                            print("Unexpected server response.")
        else:
            print("Invalid command")
