import os
from os import listdir
from os.path import isfile, join

def generate_directory(shoe):
    dirname = os.path.join(os.path.dirname(__file__), "images", shoe)
    onlyfiles = [f for f in listdir(dirname) if isfile(join(dirname, f))]
    f = open(os.path.join(dirname, "directory.txt"), 'w+')
    f2 = open(os.path.join(os.path.dirname(__file__), "directories", f"{shoe}-directory.txt"), 'w+')
    for file in onlyfiles:
        if ".jpg" not in file:
            continue
        print(file, file=f)
        print(file, file=f2)
        


if __name__ == "__main__":
    generate_directory("adidas")
    generate_directory("nike")
    generate_directory("puma")
    generate_directory("underarmor")

