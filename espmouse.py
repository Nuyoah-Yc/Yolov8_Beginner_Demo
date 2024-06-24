import socket
import time
from pynput import mouse
import threading

flag = False
timestap = 0.002

def yq(client_socket):
    while True:
        if flag:
            client_socket.sendall('m 0 1\n'.encode('utf-8'))
        time.sleep(timestap)

def on_click(x, y, button, pressed):
    global flag
    if button == mouse.Button.left:
        if pressed:
            flag = True
        else:
            flag = False

def handle_client_connection(client_socket):
    thread = threading.Thread(target=yq, args=(client_socket,))
    thread.start()
    try:
        with mouse.Listener(on_click=on_click) as listener:
            while True:
                global timestap
                timestap = float(input())
    except KeyboardInterrupt:
        print("Program terminated using Ctrl+C")
        listener.stop()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 服务器地址和端口号
    server_address = ('192.168.20.166', 1234)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print(f"Server listening on {server_address}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client_connection, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()
