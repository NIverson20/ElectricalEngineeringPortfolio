# Computer Communication Networks Project: File Transfer System

## Project Overview

This project was part of my Computer Communication Networks class, where I developed a file transfer system to transfer files between a client and server using Linux. The system utilizes both TCP and Stop-and-Wait (SNW) transfer protocols to ensure reliable communication and data integrity.

## Objectives

- **Implement File Transfer System:** Create a robust system for file transmission using Python.
- **Utilize TCP and SNW Protocols:** Implement the core functionalities of TCP and custom SNW protocols to handle file transfers.
- **Develop Client, Cache, and Server Modules:** Structure the system into three main components to manage different aspects of the data transfer process.

## My Role

- **Client Implementation:** Developed the client side of the application to initiate file transfer requests and handle responses.
- **Cache Management:** Implemented caching mechanisms to optimize data retrieval and reduce server load.
- **Server Design:** Created the server side to handle incoming requests, perform data transmissions, and manage concurrent client connections.
- **Protocol Integration:** Integrated both TCP and SNW protocols into the system to compare their efficiency and reliability.

## System Architecture

- **Client:** Manages user interface and request initiation.
- **Cache:** Temporarily stores frequently accessed files to speed up future requests.
- **Server:** Responds to client requests by sending the requested files.
- **SNW Transport:** Implements the Stop-and-Wait protocol for error checking and flow control.
- **TCP Transport:** Uses the TCP protocol for reliable data transfer.

## Challenges and Solutions

One of the key challenges was ensuring the reliability and efficiency of the SNW protocol, which required careful handling of timeouts and acknowledgments. This was addressed by:
- Implementing robust error checking and recovery mechanisms.
- Designing the protocol to efficiently handle packet loss and delays.

## Results and Impact

The implementation successfully demonstrated the use of both TCP and SNW protocols in a controlled environment, highlighting the trade-offs between complexity and reliability. This project provided deep insights into network protocol design and their practical implications in real-world applications.

## Code Snippets

Below are some excerpts from the project's codebase, showcasing the implementation of the client, cache, and server modules, as well as the transport protocols.


## Code Snippets

Below are some excerpts from the project's codebase, showcasing the implementation of the client, cache, and server modules, as well as the transport protocols.

# Sample from client.py
```python
import socket

def send_file(filename):
    s = socket.socket()
    s.connect(("localhost", 8080))
    with open(filename, 'rb') as f:
        data = f.read()
        s.sendall(data)
    s.close()
```

# Sample from cache.py
```pyton
class Cache:
    def __init__(self):
        self.files = {}

    def get_file(self, filename):
        return self.files.get(filename, None)

    def store_file(self, filename, data):
        self.files[filename] = data
```

# Sample from server.py
```pyton
import socket

def handle_client(conn):
    with open('received_file', 'wb') as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
    conn.close()
```
# Sample from snw_transport.py
```pyton
def send_snw(data, timeout=2):
    ack_received = False
    while not ack_received:
        # Send packet
        # Wait for acknowledgment
        # Resend if timeout
```
# Sample from tcp_transport.py
```python
import socket

def send_tcp(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(data)
    s.close()
```

## Full Code

The complete source code for this project is available in this repository. You can view and download the code files using the links below:

- [Client Module Code](/code/computer_comm_networks_project_code/cache.py)
- [Cache Module Code](/code/computer_comm_networks_project_code/cache.py)
- [Server Module Code](/code/computer_comm_networks_project_code/server.py)
- [SNW Transport Protocol Code](/code/computer_comm_networks_project_code/snw_transport.py)
- [TCP Transport Protocol Code](/code/computer_comm_networks_project_code/tcp_transport.py)

These files contain all the implementation details for the file transfer system using TCP and SNW protocols.
