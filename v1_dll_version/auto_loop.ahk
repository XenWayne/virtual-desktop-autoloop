#Requires AutoHotkey v1.1.33+
#SingleInstance Force
#NoEnv
#KeyHistory 0
SetWorkingDir %A_ScriptDir%
SendMode Input

; Global variables for auto-switching
IniRead, autoSwitchStr, %A_ScriptDir%\config.ini, settings, AutoSwitchEnabled, true  ; 从 config.ini 读取 AutoSwitchEnabled
AutoSwitchEnabled := (autoSwitchStr = "true")
IniRead, SwitchInterval, %A_ScriptDir%\config.ini, settings, SwitchInterval, 10000  ; 从 config.ini 读取 SwitchInterval，默认值为 10000

; 自动启动
if (AutoSwitchEnabled) {
    SetTimer, AutoSwitchDesktop, %SwitchInterval%
    OutputDebug, [AutoSwitch] Started with interval: %SwitchInterval% ms
    TrayTip, 虚拟桌面轮播工具`n@Wayne Wu | xenwayne@foxmail.com`n, 自动切换已开启，间隔 %SwitchInterval% 毫秒, 1500, 1
    Menu, Tray, Tip, 虚拟桌面轮播工具`n@Wayne Wu | xenwayne@foxmail.com`nBased on windows-desktop-switcher & AutoHotKey`n当前状态: 已开启`n切换间隔: %SwitchInterval% 毫秒
}

; Include the desktop switcher functionality
#Include desktop_switcher.ahk

; F12 toggle for auto-switching
!F12::
    AutoSwitchEnabled := !AutoSwitchEnabled
    if (AutoSwitchEnabled) {
        SetTimer, AutoSwitchDesktop, %SwitchInterval%
        OutputDebug, [AutoSwitch] Started with interval: %SwitchInterval% ms
        TrayTip, 虚拟桌面轮播工具`n@Wayne Wu | xenwayne@foxmail.com`n, 自动切换已开启，间隔 %SwitchInterval% 毫秒, 1500, 1
        Menu, Tray, Tip, 虚拟桌面轮播工具`n@Wayne Wu | xenwayne@foxmail.com`nBased on windows-desktop-switcher & AutoHotKey`n当前状态: 已开启`n切换间隔: %SwitchInterval% 毫秒
    } else {
        SetTimer, AutoSwitchDesktop, Off
        OutputDebug, [AutoSwitch] Stopped
        TrayTip, 虚拟桌面轮播工具`n@Wayne Wu | xenwayne@foxmail.com`n, 自动切换已关闭, 1500, 1
        Menu, Tray, Tip, 虚拟桌面轮播工具`n@Wayne Wu | xenwayne@foxmail.com`nBased on windows-desktop-switcher & AutoHotKey`n当前状态: 已停止`n切换间隔: %SwitchInterval% 毫秒
    }
return

; Auto-switch function
AutoSwitchDesktop:
    switchDesktopToRight()
return

; Optional: You can adjust the interval with hotkeys if needed
; F11 to decrease interval by 1 second
!F11::
    if (SwitchInterval > 1000) {
        SwitchInterval -= 1000
        if (AutoSwitchEnabled) {
            SetTimer, AutoSwitchDesktop, %SwitchInterval%
        }
        OutputDebug, [AutoSwitch] Interval decreased to: %SwitchInterval% ms
        Menu, Tray, Tip, 虚拟桌面轮播工具`n@Wayne Wu | xenwayne@foxmail.com`nBased on windows-desktop-switcher & AutoHotKey`n当前状态: 已开启`n切换间隔: %SwitchInterval% 毫秒
    }
return

; F10 to increase interval by 1 second
!F10::
    SwitchInterval += 1000
    if (AutoSwitchEnabled) {
        SetTimer, AutoSwitchDesktop, %SwitchInterval%
    }
    OutputDebug, [AutoSwitch] Interval increased to: %SwitchInterval% ms
    Menu, Tray, Tip, 虚拟桌面轮播工具`n@Wayne Wu | xenwayne@foxmail.com`nBased on windows-desktop-switcher & AutoHotKey`n当前状态: 已开启`n切换间隔: %SwitchInterval% 毫秒
return