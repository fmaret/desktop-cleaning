import time

import commctrl as cc
import win32gui as wgui

SEARCH_CRITERIA = (
    (0, "Progman", None),
    (0, "SHELLDLL_DefView", None),
    (0, "SysListView32", None),
)


class Window:
    def __init__(self):
        window = 0

        for crit in SEARCH_CRITERIA:
            window = wgui.FindWindowEx(window, *crit)

            if window == 0:
                raise Exception(
                    "Could not find child matching criteria: {:}".format(crit))

        self.window = window
    
    def get_icons_length(self):
        count = wgui.SendMessage(self.window, cc.LVM_GETITEMCOUNT, 0, 0) 

        return count


    def moveIcon(self, index: int, x: int, y: int):
        lparam = y << 16 | x

        wgui.SendMessage(self.window, cc.LVM_SETITEMPOSITION, index, lparam)


if __name__ == "__main__":
    window = Window()

    index = 1
    
    count = window.get_icons_length()
    print(count)

    # for i in range(count):
    #     x = wgui.SendMessage(window.window, cc.LVM_UPDATE, i, 0)

    u = wgui.SendMessage(window.window, cc.LVM_REDRAWITEMS, 1, count)
    print(u)

    x = 1620
    y = 1080

    window.moveIcon(2, x, y)

    time.sleep(0.1)