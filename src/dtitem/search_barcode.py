import numpy as np
import cv2 as cv
import os
import logging
import datetime
from pyzbar.pyzbar import (decode, ZBarSymbol)

from dtitem.config import (get_config)
from dtitem.utility import (Barcode)
from dtitem.crop_rect import (crop_rect)


def search_barcode_item(item, config = None):
    if config is None:
        config = get_config()

    logger = None

    text_log = config["Logging"].getboolean("text_log")
    img_log = config["Logging"].getboolean("img_log")
    show_img = config["Logging"].getboolean("show_img")
    config["Logging"]["log_path"] = config["Logging"]["log_path"].format(date_time=str(datetime.datetime.today()))
    log_path = config["Logging"]["log_path"]
    margin_x = config["Barcode"].getint("margin_x")
    margin_y = config["Barcode"].getint("margin_y")

    if img_log:
        if not os.path.exists(log_path + item.name + "/"):
            os.makedirs(log_path + item.name + "/")
    if text_log:
        logger = logging.getLogger("SEARCH_BARCODE")
        logger.info("Module SEARCH_BARCODE started")

    def logging_action(name, image):
        if show_img:
            cv.imshow(name, image)
        if img_log:
            cv.imwrite(log_path + item.name + "/" + name + ".jpg", image)
        if text_log:
            logger.info(repr(name) + " saved on " + repr(log_path + item.name + "/" + name + ".jpg"))

    gray = cv.cvtColor(item.img, cv.COLOR_BGR2GRAY)

    logging_action("1-gray.jpg", gray)

    grad_x = cv.Sobel(gray, ddepth=cv.CV_32F, dx=1, dy=0, ksize=-1)

    logging_action("2-dx.jpg", grad_x)


    gradient = cv.convertScaleAbs(grad_x)

    logging_action("3-gradient.jpg", gradient)

    blurred = cv.GaussianBlur(gradient, (1, 45), 0)
    (_, thresh) = cv.threshold(blurred, 225, 255, cv.THRESH_BINARY)

    logging_action("4-thresh.jpg", thresh)

    # construct a closing kernel and apply it to the thresholded image
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (17, 1))
    closed = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)

    logging_action("5-closed.jpg", closed)

    closed = cv.erode(closed, None, iterations=4)
    closed = cv.dilate(closed, None, iterations=4)

    logging_action("6-dilate.jpg", closed)

    (cnts, _) = cv.findContours(closed.copy(), cv.RETR_EXTERNAL,
                                cv.CHAIN_APPROX_SIMPLE)
    max_rect = cv.minAreaRect(cnts[0])
    max_area = int(max_rect[1][0] * max_rect[1][1])
    for cnt in cnts:
        rect = cv.minAreaRect(cnt)  # пытаемся вписать прямоугольник
        area = int(rect[1][0] * rect[1][1])
        if area > max_area:
            max_area = area
            max_rect = rect
    max_rect = ((max_rect[0][0], max_rect[0][1]),
                (max_rect[1][0] + 2 * margin_x, max_rect[1][1] + 2 * margin_y),
                max_rect[2])
    box = cv.boxPoints(max_rect)  # поиск четырех вершин прямоугольника
    box = np.int0(box)  # округление координат
    img_copy = item.img.copy()

    if img_log:
        cv.drawContours(img_copy, [box], 0, (255, 0, 0), 2)

    img_crop = crop_rect(item.img, max_rect)

    logging_action("7-barcode.jpg", img_crop)

    barcode = decode(img_crop,  symbols=[ZBarSymbol.EAN13])

    logging_action("8-dest.jpg", img_copy)
    if show_img:
        cv.waitKey()
        cv.destroyAllWindows()
    if len(barcode) > 0:
        item.barcode = Barcode(barcode[0].data.decode("utf-8"), max_rect, box, img_crop)
    else:
        item.barcode = Barcode(None, max_rect, box, img_crop)
    return item
