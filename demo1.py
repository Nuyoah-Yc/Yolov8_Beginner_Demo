from pynput.mouse import Controller
import time

# 初始化鼠标控制器
mouse = Controller()

# 提供的 XY 轴数据，可以是一个列表或其他结构
xy_data = [(100, 0), (0, 100), (-100, 0), (0, -100)]

# 遍历 XY 数据并移动鼠标
for x, y in xy_data:
    mouse.move(x, y)  # 从当前位置相对移动
    time.sleep(0.4)  # 暂停以观察效果
