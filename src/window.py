#!/usr/bin/env python

import time
import commctrl as cc
import win32gui as wgui
import pyautogui as pag
import os

pag.FAILSAFE = False

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

    def refresh_icons(self):
        pag.click(x=99999, y=99999)

        pag.keyDown("shift")
        pag.press("f10")
        pag.keyUp('shift')

        pag.press("down", 3)
        pag.press("enter")


if __name__ == "__main__":
    window = Window()

    index = 1

    count = window.get_icons_length()
    print(count)

    window.refresh_icons()

    x = 1920
    y = 1080

    for i in range(2):
        window.moveIcon(i, x, y)

    time.sleep(0.1)
