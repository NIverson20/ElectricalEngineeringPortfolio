import socket
import os


# get file data from server and send it
def receive_file_from_server(client_socket):
    source = client_socket.recv(6).decode()  # where the file is coming from

    file_size = int(client_socket.recv(16).strip())  # get the file size
    data = b""
    while len(data) < file_size:  # for the file size send the file
        packet = client_socket.recv(file_size - len(data))
        if not packet:
            break
        data += packet
    return source, data


# send the file to the server
def send_file_to_server(client_socket, filepath):
    with open(filepath, 'rb') as file:
        file_data = file.read()
        base_filename = os.path.basename(filepath)  # get file name only
        client_socket.sendall(b"PUT")  # send the put command for the server
        client_socket.sendall(base_filename.encode() + b"\n")  # send the file name to save as

        confirmation = client_socket.recv(18)  # confirm file length received
        if confirmation == b"FILENAME RECEIVED":
            client_socket.sendall(f"{len(file_data):<16}".encode())  # send file size
            client_socket.sendall(file_data)  # send file data
            return True
    return False


# send file to client
def send_file(conn, filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            file_data = f.read()  # send the file data
            conn.sendall(f"{len(file_data):<16}".encode())
            conn.sendall(file_data)
    else:
        conn.sendall(b"0000000000000000")  # file not found


# get file from server if cache does not have it
def forward_request_to_server(filename, SERVER_IP, SERVER_PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_client:
        server_client.connect((SERVER_IP, SERVER_PORT))
        server_client.sendall(b"GET")  # send the get command to server
        server_client.sendall(filename.encode())  # send file name

        # get the file data from the server and send to the cache
        file_size = int(server_client.recv(16).strip())
        data = b""
        # send the file data to cache
        while len(data) < file_size:
            packet = server_client.recv(file_size - len(data))
            if not packet:
                break
            data += packet
    
        if data:
            with open(filename, "wb") as f:
                f.write(data)
        return data
