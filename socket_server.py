import socket
import threading

# 创建一个socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 9999))
server_socket.listen(5)

def handle_client(client_socket):
    while True:
        try:
            # 接收客户端发送的数据
            data = client_socket.recv(1024)
            if not data:
                break
            # 解析鼠标 x 轴和 y 轴的数据
            x, y = data.decode().split(',')
            print(f"鼠标位置 - X: {x}, Y: {y}")
        except ConnectionResetError:
            break
        except Exception as e:
            print(f"错误: {e}")
            break
    client_socket.close()
    print("连接已关闭")

while True:
    print("等待连接...")
    client_socket, client_address = server_socket.accept()
    print('收到连接来自', client_address)
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
