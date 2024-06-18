import time
import mss
import screeninfo
from PIL import Image

# 获取所有显示器的信息
monitors = screeninfo.get_monitors()

# 选择主显示器（通常是第一个显示器）
main_monitor = monitors[0]

def capture_center_region(scale=0.2, save_path='screenshot.png'):

    # 开始计时
    start_time = time.time()

    # 获取主显示器的尺寸
    screen_width = main_monitor.width
    screen_height = main_monitor.height
    print(screen_width, screen_height)
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

    # 结束计时
    end_time = time.time()

    # 计算并打印截图时间（毫秒）
    elapsed_time_ms = (end_time - start_time) * 1000
    print(f'Captured screenshot in {elapsed_time_ms:.2f} milliseconds')
    print('----------------------------------------------------------------')
    # 保存截图
    img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
    img.save(save_path)
    print(f'Screenshot saved to {save_path}')



while True:
#     调用函数进行截图
    capture_center_region()