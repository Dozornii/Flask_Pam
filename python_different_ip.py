import socket

# Set the destination IP address and port
destination_ip = '127.0.0.1'
destination_port = 5000

# Set your source IP address as 127.0.0.2
source_ip = '127.0.0.2'

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the source IP address
sock.bind((source_ip, 0))

# Connect to the server
sock.connect((destination_ip, destination_port))

# Construct the HTTP GET request for the login page
request = (
    f"GET /login HTTP/1.1\r\n"
    f"Host: {destination_ip}:{destination_port}\r\n"
    f"Connection: close\r\n\r\n"
).encode()

# Send the request
sock.sendall(request)

# Receive the response
response = b''
while True:
    chunk = sock.recv(4096)
    if not chunk:
        break
    response += chunk

# Print the response
print(response.decode())

# Close the socket
sock.close()
