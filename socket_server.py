import socket
import threading
import json

# 创建一个socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 9999))
server_socket.listen(5)

def handle_client(client_socket):
    buffer = ""
    while True:
        try:
            # 接收客户端发送的数据
            data = client_socket.recv(1024)
            if not data:
                break
            buffer += data.decode()
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                # 解析鼠标 x 轴和 y 轴的数据
                data_dict = json.loads(line)
                x = data_dict['x']
                y = data_dict['y']
                print(f"\r鼠标位置 - X: {x}, Y: {y}",end="")
        except ConnectionResetError:
            break
        except json.JSONDecodeError:
            print("JSON 解析错误")
            break
        except Exception as e:
            print(f"错误: {e}")
            break
    client_socket.close()
    print(f"{client_address}连接已关闭")

while True:
    print("等待连接...")
    client_socket, client_address = server_socket.accept()
    print('收到连接来自', client_address)
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
