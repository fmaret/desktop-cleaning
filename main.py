#!/usr/bin/env python

import sys
import time
import os
import re

import commctrl as cc
import win32gui as wgui

from enum import Enum

DESKTOP_PATH = os.environ["HOMEPATH"] + "/Desktop"

class Folders(Enum):
  GAMES: str = "Games"
  APPS: str = "Apps"
  DOCUMENTS: str = "Documents"
  LAUNCHERS: str = "Launchers"

class Extension(Enum):
  URL = "url"
  LNK = "lnk"
  EXE = "exe"

def readLinesTxt(path: str):
  lines = []
  for line in open(path):
    if line.startswith("#"):
      continue

    lines.append(line.strip())

    if not line:
      continue
    
  return lines 


  
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

apps = readLinesTxt("./apps.txt")
launchers = readLinesTxt("./launchers.txt")

def isInList(file: str, list_: list[str]):
  file = ".".join(file.split(".")[:-1])

  print(file)
  
  for item in list_:
    regex = r"\b(" + item.lower() + r")\b"
    if bool(re.match(regex, file.lower().replace(u'\xa0', u' '))):
      return True

  return False


def isGame(file: str):
  return file.endswith(".url") or (file.endswith(".lnk") and not isInList(file, apps) and not isInList(file, launchers))
  
def isApp(file: str):
  return file.endswith(".lnk")

def isLauncher(file: str):
  return (file.endswith(".lnk") and isInList(file, launchers))
  
def getType(file):
  if isGame(file):
    return Folders.GAMES.value
  elif isLauncher(file):
    return Folders.LAUNCHERS.value
  elif isApp(file):
    return Folders.APPS.value
  elif file.split(".")[1]:
      return Folders.DOCUMENTS.value

def sortFiles():
  files = os.listdir(DESKTOP_PATH)

  for folder in Folders:  
    # Create folder if it doesn't exist
    if not os.path.exists(DESKTOP_PATH + "/" + folder.value):
      os.makedirs(DESKTOP_PATH + "/" + folder.value)

  print(files)
  for file in [file for file in files if len(file.split(".")) > 1]: 
    print(file)
    os.rename(DESKTOP_PATH + "/" + file, DESKTOP_PATH + "/" + getType(file) +"/"+ file)
  return 
  
def main(*argv):
    wnd = getWnd()
    idx = 1

    sortFiles()

    wgui.SendMessage(wnd, cc.LVM_UPDATE, idx, 0)

    x = 1920
    y = 1080

    moveTo(x, y, 1)
    
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