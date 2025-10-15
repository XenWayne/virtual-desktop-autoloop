from pynput.keyboard import Key, Controller, Listener
import time
import threading
import ctypes
import configparser
import pystray
from PIL import Image, ImageDraw

keyboard = Controller()

# 修改：读取配置文件中的等待间隔（config.ini 文件中 [settings] 节的 interval 参数）
def get_sleep_interval():
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        return config.getfloat("settings", "interval", fallback=2.0)
    except Exception:
        return 2.0

# 新增：最小化控制台窗口（仅适用于 Windows）
def minimize_console():
    SW_MINIMIZE = 6
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), SW_MINIMIZE)

running = True

# 修改：每次循环检查 running 状态，并读取等待间隔
def press_keys():
    global running
    while True:
        if running:
            # 按下左Shift
            keyboard.press(Key.shift)
            # 按下Alt
            keyboard.press(Key.alt)
            # 按下右箭头
            keyboard.press(Key.right)
            
            # 释放右箭头
            keyboard.release(Key.right)
            # 释放Alt
            keyboard.release(Key.alt)
            # 释放左Shift
            keyboard.release(Key.shift)
            
            # 每次循环读取配置文件控制的等待间隔
            interval = get_sleep_interval()
            time.sleep(interval)
        else:
            time.sleep(2)

# 新增：快捷键 F9 切换启停状态
def on_press(key):
    global running
    try:
        if key == Key.f9:
            running = not running
            print("Toggled running:", running)
    except AttributeError:
        pass

# 修改：创建托盘图标图像
def create_image():
    # 生成一个新的图标：蓝色背景，白色文本 "AK"
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color='blue')
    dc = ImageDraw.Draw(image)
    dc.text((10, 25), "AK", fill="white")
    return image

# 新增：退出应用程序的回调
def exit_app(icon, item):
    icon.stop()
    import os
    os._exit(0)

if __name__ == "__main__":
    minimize_console()
    # 后台线程运行自动按键操作函数
    t = threading.Thread(target=press_keys, daemon=True)
    t.start()
    # 启动键盘监听等待 F9 切换启停状态
    listener = Listener(on_press=on_press)
    listener.start()
    # 新增：创建托盘图标并添加退出菜单
    menu = pystray.Menu(pystray.MenuItem("退出", exit_app))
    icon = pystray.Icon("AutoKey", create_image(), "Auto Key", menu)
    icon.run()