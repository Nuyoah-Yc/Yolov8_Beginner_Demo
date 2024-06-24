import json
import socket
import torch
import mss
import screeninfo
from PIL import Image
from ultralytics import YOLO
from pynput import mouse
from pynput.mouse import Controller
import threading

class ScreenObjectDetector:
    def __init__(self, model_path='data/yolov8n.pt', ip='10.11.12.17', port=9999):
        # 初始化 YOLO 模型
        self.model = YOLO(model_path)
        # 检查并设置设备为 GPU 或 CPU
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        # 获取主显示器
        self.main_monitor = screeninfo.get_monitors()[0]
        # 设置服务器连接
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        # 右键监听标志
        self.detecting = False
        # 初始化鼠标控制器
        self.mouse_controller = Controller()

        # 启动右键监听
        listener = mouse.Listener(on_click=self.on_click)
        listener.start()

        # 启动目标检测线程
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.right:
            if pressed:
                print("Right button pressed")
                self.detecting = True
            else:
                print("Right button released")
                self.detecting = False

    def capture_center_region(self, scale=0.2):
        # 获取和计算屏幕中心区域的尺寸和位置
        screen_width = self.main_monitor.width
        screen_height = self.main_monitor.height
        region_width = int(screen_width * scale)
        region_height = int(screen_height * scale)
        left = self.main_monitor.x + (screen_width - region_width) // 2
        top = self.main_monitor.y + (screen_height - region_height) // 2
        # 截图
        with mss.mss() as sct:
            monitor = {"left": left, "top": top, "width": region_width, "height": region_height}
            screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        return img, region_width, region_height

    def run(self):
        while True:
            if self.detecting:
                img, w, h = self.capture_center_region()
                results = self.model.predict(source=img, device=self.device, verbose=False, classes=[0])
                for image_result in results:
                    # 处理检测结果
                    xyxy_array = image_result.boxes.xyxy.cpu().numpy().astype("uint32")
                    if xyxy_array is not None and len(xyxy_array) > 0:
                        center_x = int((xyxy_array[0][0] + xyxy_array[0][2]) // 2 - w // 2)
                        center_y = int((xyxy_array[0][1] + xyxy_array[0][3]) // 2 - h // 2)
                        data_json = {"x": center_x, "y": center_y}
                        json_str = json.dumps(data_json)
                        print(f"\rSending JSON: {json_str}", end="")
                        self.socket.send((json_str + '\n').encode("utf-8"))
                        # 移动鼠标到目标位置
                        self.mouse_controller.move(center_x, center_y)

if __name__ == "__main__":
    detector = ScreenObjectDetector()
