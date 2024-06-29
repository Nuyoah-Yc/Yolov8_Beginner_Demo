import socket
import time

# 连接到服务器
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('192.168.120.114', 9999))
a = 0
try:
    while True:
        a += 1
        data = f"Hello, world!{a}"

        if not data:
            print("输入不能为空，请重新输入。")
            continue

        s.send(data.encode('utf-8'))

        # 接收服务器返回的消息
        data = s.recv(1024)
        print("服务器返回的消息：", data.decode('utf-8'))

        # 每隔1秒发送一次消息
        time.sleep(1)

finally:
    s.close()
