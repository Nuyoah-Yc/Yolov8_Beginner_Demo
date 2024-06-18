import time
import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image


def capture_screenshot(width, height):
    # 创建帧缓冲区对象
    framebuffer = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, framebuffer)

    # 创建纹理对象
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture, 0)

    # 检查帧缓冲区是否完整
    if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
        raise RuntimeError('Framebuffer not complete')

    # 读取像素数据
    glReadBuffer(GL_COLOR_ATTACHMENT0)
    pixels = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)

    # 清理资源
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glDeleteFramebuffers(1, [framebuffer])
    glDeleteTextures(1, [texture])

    return pixels

def main():
    width, height = 1920, 1080

    # 初始化 OpenGL 窗口
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"OpenGL Window")

    # 捕获截图
    start_time = time.time()
    pixels = capture_screenshot(width, height)
    end_time = time.time()

    # 将像素数据转换为图像
    image = Image.frombytes("RGB", (width, height), pixels)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL 的原点在左下角，需要翻转图像
    image.save("screenshot.png")

    print(f"Captured screenshot in {(end_time - start_time) * 1000:.2f} milliseconds")
    print("Screenshot saved to screenshot.png")

if __name__ == "__main__":
    main()
