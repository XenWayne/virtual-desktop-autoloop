#Requires AutoHotkey v1.1.33+
#SingleInstance Force
#NoEnv
#KeyHistory 0
SetWorkingDir %A_ScriptDir%
SendMode Input

; Global variables for auto-switching
IniRead, autoSwitchStr, %A_ScriptDir%\config.ini, settings, AutoSwitchEnabled, true  ; �� config.ini ��ȡ AutoSwitchEnabled
AutoSwitchEnabled := (autoSwitchStr = "true")
IniRead, SwitchInterval, %A_ScriptDir%\config.ini, settings, SwitchInterval, 10000  ; �� config.ini ��ȡ SwitchInterval��Ĭ��ֵΪ 10000

; �Զ�����
if (AutoSwitchEnabled) {
    SetTimer, AutoSwitchDesktop, %SwitchInterval%
    OutputDebug, [AutoSwitch] Started with interval: %SwitchInterval% ms
    TrayTip, ���������ֲ�����`n@Wayne Wu | xenwayne@foxmail.com`n, �Զ��л��ѿ�������� %SwitchInterval% ����, 1500, 1
    Menu, Tray, Tip, ���������ֲ�����`n@Wayne Wu | xenwayne@foxmail.com`nBased on windows-desktop-switcher & AutoHotKey`n��ǰ״̬: �ѿ���`n�л����: %SwitchInterval% ����
}

; Include the desktop switcher functionality
#Include desktop_switcher.ahk

; F12 toggle for auto-switching
!F12::
    AutoSwitchEnabled := !AutoSwitchEnabled
    if (AutoSwitchEnabled) {
        SetTimer, AutoSwitchDesktop, %SwitchInterval%
        OutputDebug, [AutoSwitch] Started with interval: %SwitchInterval% ms
        TrayTip, ���������ֲ�����`n@Wayne Wu | xenwayne@foxmail.com`n, �Զ��л��ѿ�������� %SwitchInterval% ����, 1500, 1
        Menu, Tray, Tip, ���������ֲ�����`n@Wayne Wu | xenwayne@foxmail.com`nBased on windows-desktop-switcher & AutoHotKey`n��ǰ״̬: �ѿ���`n�л����: %SwitchInterval% ����
    } else {
        SetTimer, AutoSwitchDesktop, Off
        OutputDebug, [AutoSwitch] Stopped
        TrayTip, ���������ֲ�����`n@Wayne Wu | xenwayne@foxmail.com`n, �Զ��л��ѹر�, 1500, 1
        Menu, Tray, Tip, ���������ֲ�����`n@Wayne Wu | xenwayne@foxmail.com`nBased on windows-desktop-switcher & AutoHotKey`n��ǰ״̬: ��ֹͣ`n�л����: %SwitchInterval% ����
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
        Menu, Tray, Tip, ���������ֲ�����`n@Wayne Wu | xenwayne@foxmail.com`nBased on windows-desktop-switcher & AutoHotKey`n��ǰ״̬: �ѿ���`n�л����: %SwitchInterval% ����
    }
return

; F10 to increase interval by 1 second
!F10::
    SwitchInterval += 1000
    if (AutoSwitchEnabled) {
        SetTimer, AutoSwitchDesktop, %SwitchInterval%
    }
    OutputDebug, [AutoSwitch] Interval increased to: %SwitchInterval% ms
    Menu, Tray, Tip, ���������ֲ�����`n@Wayne Wu | xenwayne@foxmail.com`nBased on windows-desktop-switcher & AutoHotKey`n��ǰ״̬: �ѿ���`n�л����: %SwitchInterval% ����
return