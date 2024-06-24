from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Listener

mouse = Controller()

# 移动鼠标到指定位置
mouse.position = (100, 100)

# 从当前位置相对移动
mouse.move(50, 50)

# 点击鼠标
mouse.click(Button.left, 1)

# 键盘事件监听
def on_press(key):
    print(f'{key} pressed')

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# 鼠标监听事件

