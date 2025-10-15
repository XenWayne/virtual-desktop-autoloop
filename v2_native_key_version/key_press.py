"""
VDM快捷键触发器V1.0\nWorks with VirtualDesktopManager Alternative Mode
@Wayne Wu | xenwayne@foxmail.com
Based on windows-desktop-switcher & AutoHotKey
"""

from pynput.keyboard import Key, Controller, Listener
import time
import threading
import ctypes
import configparser
import pystray
from PIL import Image

keyboard = Controller()

# 读取配置文件中的等待间隔（config.ini 文件中 [settings] 节的 interval 参数）
def get_sleep_interval():
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        return config.getfloat("settings", "interval", fallback=10.0)
    except Exception:
        return 10.0

# 新增：最小化控制台窗口（仅适用于 Windows）
def minimize_console():
    SW_MINIMIZE = 6
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), SW_MINIMIZE)

running = True
tray_icon = None  # 新增全局变量，用于保存托盘图标对象

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

# 快捷键 F9 切换启停状态，同时更新托盘图标的标题（中文提示，包含作者信息）
def on_press(key):
    global running, tray_icon
    try:
        if key == Key.f9:
            running = not running
            print("Toggled running:", running)
            if tray_icon is not None:
                tray_icon.title = f"VDM快捷键触发器V1.0\nWorks with VirtualDesktopManager Alternative Mode\n@Wayne Wu | xenwayne@foxmail.com\n{'运行中' if running else '已暂停'} - 启停快捷键: F9"
    except AttributeError:
        pass

# 修改：创建托盘图标函数，改为使用本文件夹下的 icon.ico 文件
def create_image():
    return Image.open("icon.ico")

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
    # 创建托盘图标时设置初始标题为中文状态、快捷键信息和作者信息
    menu = pystray.Menu(pystray.MenuItem("退出", exit_app))
    tray_icon = pystray.Icon(
        "AutoKey", 
        create_image(), 
        f"VDM快捷键触发器V1.0\nWorks with VirtualDesktopManager Alternative Mode\n@Wayne Wu | xenwayne@foxmail.com\n{'运行中' if running else '已暂停'} - 启停快捷键: F9", 
        menu
    )
    tray_icon.run()