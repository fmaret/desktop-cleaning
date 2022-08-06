import time

import commctrl as cc
import win32gui as wgui

def getWnd():
    search_criteria = (
        (0, "Progman", None),
        (0, "SHELLDLL_DefView", None),
        (0, "SysListView32", None),
    )

    wnd = 0
    for crit in search_criteria:
        wnd = wgui.FindWindowEx(wnd, *crit)
        if wnd == 0:
            print("Could not find child matching criteria: {:}".format(crit))
            return wnd
    return wnd


def moveTo(x: int, y: int, index: int):
    wnd = getWnd()

    lparam = y << 16 | x

    wgui.SendMessage(wnd, cc.LVM_SETITEMPOSITION, index, lparam)

if __name__ == "__main__":
    wnd = getWnd()
    idx = 1


    wgui.SendMessage(wnd, cc.LVM_UPDATE, idx, 0)

    x = 1920
    y = 1080

    moveTo(x, y, 1)

    time.sleep(0.1)

    item_count = wgui.SendMessage(wnd, cc.LVM_GETITEMCOUNT, 0, 0)