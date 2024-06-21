import socket


# 创建一个socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定IP地址和端口
server_socket.bind(('0.0.0.0', 9999))

server_socket.listen(5)

while True:
    # 等待客户端连接
    client_socket, client_address = server_socket.accept()

    # 接收客户端发送的数据
    data = client_socket.recv(1024)
    print('Got connection from', client_address)
    print('Data received:', data.decode())

