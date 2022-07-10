#!/usr/bin/env python

import msvcrt
import sys
import time
import os
import random

import commctrl as cc
import win32gui as wgui

from enum import Enum

DESKTOP_PATH = os.environ["HOMEPATH"] + "/Desktop"

class Folders(Enum):
  GAMES: str = "Games"
  APPS: str = "Apps"
  DOCUMENTS: str = "Documents"
  
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

def sortFiles():
  files = os.listdir(DESKTOP_PATH)

  for folder in Folders:
    # Create folder if it doesn't exist
    if not os.path.exists(DESKTOP_PATH + "/" + folder.value):
      os.makedirs(DESKTOP_PATH + "/" + folder.value)


  for file in [file for file in files if len(file.split(".")) == 2]: 
    if file.endswith(".url"):
      # Move it to the folder Games
      os.rename(DESKTOP_PATH + "/" + file, DESKTOP_PATH + "/" +Folders.GAMES.value +"/"+ file)
    elif file.endswith(".exe"):
      # Move it to the folder Apps
      os.rename(DESKTOP_PATH + "/" + file, DESKTOP_PATH + "/" +Folders.APPS.value +"/" + file)
    elif file.endswith(".lnk"):
      # Check if file is a game
      os.rename(DESKTOP_PATH + "/" + file, DESKTOP_PATH + "/" +Folders.APPS.value +"/" + file)
    elif file.split(".")[1]:
      # Move it to the folder Apps
      os.rename(DESKTOP_PATH + "/" + file, DESKTOP_PATH + "/" +Folders.DOCUMENTS.value +"/" + file)
  
  return 
  
def main(*argv):
    wnd = getWnd()
    idx = 1
    wgui.SendMessage(wnd, cc.LVM_UPDATE, idx, 0)

    sortFiles()


    x = 1920
    y = 1080
    
    time.sleep(0.1)


    item_count = wgui.SendMessage(wnd, cc.LVM_GETITEMCOUNT, 0, 0)
    
    

    # print(o)  

    # u = wgui.SendMessage(wnd, cc.LVM_SETCOLUMNW, 2, 500)
    # print("size:", u) 

    # resize desktop grid 



    


if __name__ == "__main__":
    rc = main(*sys.argv[1:])
    print("\nDone.")
    sys.exit(rc)