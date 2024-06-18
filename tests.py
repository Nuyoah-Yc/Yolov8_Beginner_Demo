from ultralytics import YOLO
from PIL import Image
import cv2
import torch
import time

# 加载 YOLOv8 模型
model = YOLO("data/yolov8n.pt")

# 检查并设置设备为 GPU 或 CPU
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('device:', device)

# 将模型移至设备（GPU 或 CPU）
model.to(device)

# 读取输入图像
im2 = cv2.imread("data/bus.jpg")


t1 = time.time()
results = model.predict(source=im2, device=device, verbose=False,classes=[0])
t2 = time.time()

# 计算并打印推理耗时（毫秒）
t_spend = t2 - t1
print("推理耗时：", t_spend * 1000)

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
        print(i, class_index, class_name, class_score, box)
