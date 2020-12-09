import os
from os import listdir
from os.path import isfile, join
import cv2


def flip(file):
    src = cv2.imread(file)
    flipped = cv2.flip(src, 1)
    cv2.imwrite(file, flipped)


def correct_shoes(shoe, condition):
    dirname = os.path.join(os.path.dirname(__file__), "images", shoe)
    onlyfiles = [f for f in listdir(dirname) if isfile(join(dirname, f))]
    f = open(os.path.join(dirname, "directory.txt"), 'w+')
    for file in onlyfiles:
        if condition in file:
            flip(os.path.join(dirname, file))
        


if __name__ == "__main__":
    # correct_shoes("underarmor", "DEFAULT")
    correct_shoes("adidas", "adidas")
