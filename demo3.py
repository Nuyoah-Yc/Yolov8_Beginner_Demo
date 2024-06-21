import time
import torch
import numpy as np
from PIL import Image
import mss
import screeninfo
from pynput import mouse, keyboard
from ultralytics import YOLO

# 加载 YOLOv8 模型
model = YOLO("data/yolov8n.pt")

# 检查并设置设备为 GPU 或 CPU
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('device:', device)

# 将模型移至设备（GPU 或 CPU）
model.to(device)

# 获取所有显示器的信息
monitors = screeninfo.get_monitors()

# 选择主显示器（通常是第一个显示器）
main_monitor = monitors[0]


def capture_center_region(scale=0.2):
    # 获取主显示器的尺寸
    screen_width = main_monitor.width
    screen_height = main_monitor.height

    # 计算中心区域的大小
    region_width = int(screen_width * scale)
    region_height = int(screen_height * scale)

    # 计算中心区域的左上角坐标
    left = main_monitor.x + (screen_width - region_width) // 2
    top = main_monitor.y + (screen_height - region_height) // 2

    # 使用mss进行截图
    with mss.mss() as sct:
        monitor = {
            "left": left,
            "top": top,
            "width": region_width,
            "height": region_height
        }
        screenshot = sct.grab(monitor)
    img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

    return img, region_width, region_height


# 定义一个标志以检测鼠标右键按下
right_button_down = False
# 定义一个标志以检测键盘ESC按下
esc_down = False

def on_click(x, y, button, pressed):
    global right_button_down
    if button == mouse.Button.right:
        right_button_down = pressed


def on_press(key):
    global esc_down
    if key == keyboard.Key.esc:
        esc_down = True


# 启动鼠标监听器
mouse.Listener(on_click=on_click).start()


# 启用键盘监听器
keyboard.Listener(on_press=on_press).start()

while True:
    # 捕获屏幕中心区域图像
    im2, w, h = capture_center_region()

    # 计算中心区域的中心坐标
    center_w_x = w // 2
    center_h_y = h // 2


    if right_button_down:
        # 创建透明画布
        transparent_canvas = np.zeros((h, w, 4), dtype=np.uint8)

        # 开始计时
        t1 = time.time()

        # 进行推理
        results = model.predict(source=im2, device=device, verbose=False, classes=[0])

        # 结束计时
        t2 = time.time()

        # 计算FPS
        t_spend = t2 - t1
        fps = 1 / t_spend

        # 打印FPS，并保持在同一行
        print(f"\rFPS: {fps:.2f}", end="")

        # 处理并打印每个检测结果
        for image_result in results:
            names = image_result.names
            cls_array = image_result.boxes.cls.cpu().numpy().astype("uint32")  # 类别索引
            xyxy_array = image_result.boxes.xyxy.cpu().numpy().astype("uint32")  # 坐标
            conf_array = image_result.boxes.conf.cpu().numpy().astype("float")  # 置信度

            for i in range(len(cls_array)):
                class_index = cls_array[i]
                class_name = names[class_index]
                class_score = conf_array[i]
                box = xyxy_array[i]

                # 计算中心点坐标
                center_x = (box[0] + box[2]) // 2
                center_y = (box[1] + box[3]) // 2

                # 计算相对中心点坐标
                rel_center_x = center_x - center_w_x
                rel_center_y = center_y - center_h_y

                print(f"\r{class_name}: ({rel_center_x}, {rel_center_y}) {class_score:.2f}")




mouse.Listener.stop()
keyboard.Listener.stop()
