from socket import *

server_name = 'gaia.cs.umass.edu'
server_port = 80

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

request = "GET /kurose_ross/interactive/index.php HTTP/1.1\r\nHost: gaia.cs.umass.edu\r\n\r\n"
client_socket.send(request.encode())

response = client_socket.recv(4096)
print(response.decode())

client_socket.close()
