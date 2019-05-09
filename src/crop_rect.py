import cv2 as cv
import numpy as np


def crop_rect(img, rect):
    center, size, angle = rect[0], rect[1], rect[2]
    center, size = tuple(map(int, center)), tuple(map(int, size))
    height, width = img.shape[0], img.shape[1]

    translation = np.float32([[1, 0, width/2 - center[0]], [0, 1, height/2 - center[1]]])
    img_tr = cv.warpAffine(img, translation, (width, height))
    rotation = cv.getRotationMatrix2D((width/2, height/2), angle, 1)
    img_rot = cv.warpAffine(img_tr, rotation, (width, height))

    img_crop = cv.getRectSubPix(img_rot, size, (width/2, height/2))

    if img_crop.shape[0] > img_crop.shape[1]:
        img_crop = cv.rotate(img_crop, cv.ROTATE_90_CLOCKWISE)

    return img_crop
