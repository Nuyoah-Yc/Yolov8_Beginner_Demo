import socket
import time
import torch
import mss
import screeninfo
from PIL import Image
from pynput import mouse, keyboard
from ultralytics import YOLO

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

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.right:
            self.right_button_down = pressed


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
            img, w, h = self.capture_center_region()
            results = self.model.predict(source=img, device=self.device, verbose=False, classes=[0])
            for image_result in results:
                # 处理检测结果
                xyxy_array = image_result.boxes.xyxy.cpu().numpy().astype("uint32")
                if xyxy_array is not None and len(xyxy_array) > 0:
                    center_x = (xyxy_array[0][0] + xyxy_array[0][2]) // 2 - w // 2
                    center_y = (xyxy_array[0][1] + xyxy_array[0][3]) // 2 - h // 2
                    print(f"Detected center: ({center_x}, {center_y})")
                    data_json = {"x": center_x, "y": center_y}
                    self.socket.send(str(data_json).encode())

if __name__ == "__main__":
    detector = ScreenObjectDetector()
    detector.run()
