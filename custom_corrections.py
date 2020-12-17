import os
from os import listdir
from os.path import isfile, join
import cv2
from PIL import Image
import numpy as np
import random

BLUR = 21
CANNY_THRESH_1 = 10
CANNY_THRESH_2 = 20
MASK_DILATE_ITER = 20
MASK_ERODE_ITER = 20
MASK_COLOR = (1.0,1.0,1.0) # In BGR format

def offset_gen(num_images, desired):
    print(desired // num_images)
    def random_offset(file):
        img = cv2.imread(file)
        for i in range(desired // num_images):
            background = np.zeros([276, 276, 3], dtype=np.uint8)
            background.fill(255)
            rand1 = random.randint(0, 20)
            rand2 = random.randint(0, 20)
            background[20-rand1:276-rand1, 20-rand2:276-rand2, :] = img
            background = background[10:266, 10:266, :]
            fn = file.split(".")
            fn = fn[0] + f"_{i}_{10-rand1}_{10-rand2}.jpg"
            cv2.imwrite(fn, background)
    return random_offset


def center_adidas(file):
    img_3 = np.zeros([140,256,3],dtype=np.uint8)
    img_3.fill(255)
    img = cv2.imread(file)
    new = np.vstack((img, img_3))
    shape = new.shape[0]//2
    final = new[shape-128+7:shape+128+7,:,:]
    #print(final.shape)
    #cv2.imshow('initial', img)
    #cv2.imshow('final', final)
    #cv2.waitKey()
    cv2.imwrite(file, final)


def center_nike(file):
    img_3 = np.zeros([13,256,3],dtype=np.uint8)
    img_3.fill(255)
    img = cv2.imread(file)
    new = np.vstack((img, img_3))
    shape = new.shape[0]//2
    final = new[shape-128+7:shape+128+7,:,:]
    #print(final.shape)
    #cv2.imshow('initial', img)
    #cv2.imshow('final', final)
    #cv2.waitKey()
    cv2.imwrite(file, final)


def rgba2rgb(file, background=(255,255,255) ):
    f = open(file, "rb")
    image = Image.open(f).convert("RGBA")
    rgba = np.array(image)
    row, col, ch = rgba.shape
    if ch == 3:
        Image.fromarray(np.asarray( rgba, dtype='uint8' )).save(file)
        f.close()
        return 

    assert ch == 4, 'RGBA image has 4 channels.'

    rgb = np.zeros( (row, col, 3), dtype='float32' )
    r, g, b, a = rgba[:,:,0], rgba[:,:,1], rgba[:,:,2], rgba[:,:,3]

    a = np.asarray( a, dtype='float32' ) / 255.0

    R, G, B = background

    rgb[:,:,0] = r * a + (1.0 - a) * R
    rgb[:,:,1] = g * a + (1.0 - a) * G
    rgb[:,:,2] = b * a + (1.0 - a) * B
    rgb = Image.fromarray(np.asarray( rgb, dtype='uint8' ))
    rgb.save(file)
    f.close()
    return rgb


def remove_background(file):
    # https://likegeeks.com/python-image-processing/#:~:text=To%20remove%20the%20background%20from,image%20using%20the%20bitwise_and%20operator.&text=In%20the%20threshold()%20method,the%20style%20of%20the%20threshold.
    # https://stackoverflow.com/questions/29313667/how-do-i-remove-the-background-from-this-kind-of-image
    img = cv2.imread(file)
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    #-- Create empty mask, draw filled polygon on it corresponding to largest contour ----
    # Mask is black, polygon is white
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    #-- Smooth mask, then blur it --------------------------------------------------------
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

    #-- Blend masked img into MASK_COLOR background --------------------------------------
    mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
    img         = img.astype('float32') / 255.0                 #  for easy blending

    masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 

    
    #cv2.imshow('initial', img)
    #cv2.imshow('final', masked)                                   # Display
    #cv2.waitKey()
        
    cv2.imwrite(file, masked)
    

def flip(file):
    src = cv2.imread(file)
    flipped = cv2.flip(src, 1)
    cv2.imwrite(file, flipped)


def correct_shoes(shoe, condition, func):
    dirname = os.path.join(os.path.dirname(__file__), "images", shoe)
    onlyfiles = [f for f in listdir(dirname) if isfile(join(dirname, f))]
    f = open(os.path.join(dirname, "directory.txt"), 'w+')
    for file in onlyfiles:
        if condition in file:
            func(os.path.join(dirname, file))
    return len(onlyfiles)
        
 

if __name__ == "__main__":
    print("puma not trans")
    p = correct_shoes("puma", "puma", rgba2rgb)
    
##    print("flip ua")
##    correct_shoes("underarmor", "DEFAULT", flip)
##    print("flip adidas")
##    correct_shoes("adidas", "adidas", flip)
    
    print("center nike")
    n = correct_shoes("nike", "nike", center_nike)
    print("remove background nike")
    correct_shoes("nike", "nike", remove_background)
    print("center adidas")
    a = correct_shoes("adidas", "adidas", center_adidas)
    print("remove background adidas")
    correct_shoes("adidas", "adidas", remove_background)
    print("remove background underarmor")
    u = correct_shoes("underarmor", "underarmor", remove_background)
    print("randomization nike")
    random_offset = offset_gen(n, 10000)
    correct_shoes("nike", "nike", random_offset)
    print("randomization adidas")
    random_offset = offset_gen(a, 10000)
    correct_shoes("adidas", "adidas", random_offset)
    print("randomization puma")
    random_offset = offset_gen(p, 10000)
    correct_shoes("puma", "puma", random_offset)
    print("randomization underarmor")
    random_offset = offset_gen(u, 10000)
    correct_shoes("underarmor", "underarmor", random_offset)
    

    
