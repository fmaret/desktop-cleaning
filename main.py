#!/usr/bin/env python
import os
from rules import chooseFolder

DESKTOP_PATH = os.environ["HOMEPATH"] + "/Desktop"


def sortFiles():
    files = os.listdir(DESKTOP_PATH)

    for file in [file for file in files if len(file.split(".")) > 1]:
        folder = chooseFolder(file)

        if not os.path.exists(DESKTOP_PATH + "/" + folder):
            os.makedirs(DESKTOP_PATH + "/" + folder)

        os.rename(DESKTOP_PATH + "/" + file, DESKTOP_PATH +
                  "/" + folder + "/" + file)


def emptyFolders():
    files = os.listdir(DESKTOP_PATH)

    for folder in [file for file in files if len(file.split(".")) == 1]:
        for file in os.listdir(DESKTOP_PATH + "/" + folder):
            os.rename(DESKTOP_PATH + "/" + folder + "/" +
                      file, DESKTOP_PATH + "/" + file)

        os.rmdir(DESKTOP_PATH + "/" + folder)


def main():
    emptyFolder = input("Do you want to empty folders before sorting? (y/n) ")
    if emptyFolder == "y":
      emptyFolders()
    sortFiles()


if __name__ == "__main__":
    main()
