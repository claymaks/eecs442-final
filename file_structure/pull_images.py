import requests
import os

def get_images(name, train=100, val=38, overwrite=False):
    url = "https://raw.githubusercontent.com/claymaks/eecs442-final/main/images/" + name + "/"
    directory = url + "directory.txt"
    dir_txt = requests.get(directory)
    file_paths = dir_txt.content.decode("utf-8").split('\n')
    cur_files = os.listdir(os.path.join(os.getcwd(), f"images/"))
    for n, file in enumerate(file_paths):
        if not file or (file in cur_files and not overwrite):
            continue
        img_dat = requests.get(url + file)
        if not img_dat.ok:
            print("bad image:", file)
            continue
        
        with open(f"images/{file}", "wb") as img:
            img.write(img_dat.content)
        cat = "train" if n <= train else "val" if n <= train + val else "test"
        with open(f"dataset/{cat}/{name}/{file}", "wb") as img:
            img.write(img_dat.content)

    return len(file_paths)

for shoe in ["adidas", "nike", "puma", "underarmor"]:
    print("\ndownloading from", shoe)  
    print(f"\n\tgot {get_images(shoe, overwrite=True)} images")
