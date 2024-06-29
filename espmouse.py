import socket
import time
from pynput import mouse
import threading

flag=False
timestap = 0.001

def yq():
    while(True):
        if(flag): 
            # print('Sending ')
            client_socket.sendall('m 0 1\n'.encode('utf-8'))
        time.sleep(timestap)


def on_click(x, y, button, pressed):
    global flag
    if button == mouse.Button.left:
        if pressed:
            # print(f"左键按下 at ({x}, {y})")
            client_socket.sendall('y 0 0'.encode('utf-8'))
            # flag = True
            
        else:
            # print("左键松开")
            client_socket.sendall('c 0 0'.encode('utf-8'))
            # flag = False

def main():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 服务器地址和端口号
    server_address = ('192.168.121.164', 1234)
    
    # 连接到服务器
    print('Connecting to {} port {}'.format(*server_address))
    client_socket.connect(server_address)
    thread = threading.Thread(target=yq)
    thread.start()
    try:
        with mouse.Listener(on_click=on_click) as listener:
            # listener.join() 
            while True:
                global timestap
                timestap = float(input())
    except KeyboardInterrupt:        
        print("Program terminated using Ctrl+C")
        listener.stop()
    

if __name__ == '__main__':
    main()
