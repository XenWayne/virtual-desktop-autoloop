"""
VDM快捷键触发器
@Wayne Wu | xenwayne@foxmail.com
Based on windows-desktop-switcher & AutoHotKey
"""
# 定义变量存储标题、描述和作者信息
APP_TITLE_ZH = "VDM快捷键触发器V1.0"
APP_TITLE_EN = "Works with VirtualDesktopManager Alternative Mode"
APP_AUTHOR = "@Wayne Wu | xenwayne@foxmail.com"

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

# 新增：从配置文件读取启停快捷键，默认为 F7
def get_toggle_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        return config.get("settings", "toggle_key", fallback="F7")
    except Exception:
        return "F7"

# 新增：从配置文件读取启动状态，默认为 False
def get_start_running():
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        return config.getboolean("settings", "start_running", fallback=True)
    except Exception:
        return False

running = get_start_running()
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

# 修改：使用配置文件中的启停快捷键进行判断，同时更新托盘图标标题
def on_press(key):
    global running, tray_icon
    try:
        toggle_key = get_toggle_key()
        if key == getattr(Key, toggle_key.lower()):
            running = not running
            print("Toggled running:", running)
            if tray_icon is not None:
                tray_icon.title = (
                    f"{APP_TITLE_ZH}\n"
                    f"{APP_TITLE_EN}\n"
                    f"{APP_AUTHOR}\n"
                    f"{'运行中' if running else '已暂停'} - 启停快捷键: {toggle_key.upper()}"
                )
    except AttributeError:
        pass

# 新增：退出应用程序的回调
def exit_app(icon, item):
    icon.stop()
    import os
    os._exit(0)

# 修改：创建托盘图标函数，改为使用本文件夹下的 icon.ico 文件
def create_image():
    return Image.open("icon.ico")

if __name__ == "__main__":
    minimize_console()
    # 后台线程运行自动按键操作函数
    t = threading.Thread(target=press_keys, daemon=True)
    t.start()
    # 启动键盘监听等待切换启停状态
    listener = Listener(on_press=on_press)
    listener.start()
    # 创建托盘图标时设置初始标题为中文状态、快捷键信息和作者信息
    menu = pystray.Menu(pystray.MenuItem("退出", exit_app))
    toggle_key = get_toggle_key()
    tray_icon = pystray.Icon(
        "AutoKey", 
        create_image(), 
        f"{APP_TITLE_ZH}\n{APP_TITLE_EN}\n{APP_AUTHOR}\n{'运行中' if running else '已暂停'} - 启停快捷键: {toggle_key.upper()}",
        menu
    )
    tray_icon.run()