import os
from os import listdir
from os.path import isfile, join

def generate_directory(shoe):
    dirname = os.path.join(os.path.dirname(__file__), "images", shoe)
    onlyfiles = [f for f in listdir(dirname) if isfile(join(dirname, f))]
    f = open(os.path.join(dirname, "directory.txt"), 'w+')
    for file in onlyfiles:
        print(file, file=f)


if __name__ == "__main__":
    generate_directory("adidas")
    generate_directory("nike")
    generate_directory("puma")
    generate_directory("underarmor")
