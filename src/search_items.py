import numpy as np
import cv2 as cv
import logging
import datetime
import os

from dtitem.utility import (Item)
from dtitem.config import (get_config)
from dtitem.crop_rect import (crop_rect)
from ast import literal_eval as make_tuple


def search_items(img, config=None):
    if config is None:
        config = get_config()

    logger = None

    text_log = config["Logging"].getboolean("text_log")
    img_log = config["Logging"].getboolean("img_log")
    show_img = config["Logging"].getboolean("show_img")
    config["Logging"]["log_path"] = config["Logging"]["log_path"].format(date_time=str(datetime.datetime.today()))
    log_path = config["Logging"]["log_path"]
    image_scale_factor = config["SearchItem"].getfloat("image_scale_factor")
    gaussian_kernel = make_tuple(config["SearchItem"]["gaussian_kernel"])
    sigma = config["SearchItem"].getfloat("sigma")
    close_kernel = make_tuple(config["SearchItem"]["close_kernel"])
    max_area = make_tuple(config["SearchItem"]["max_area"])

    if text_log or img_log:
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        if text_log:
            logger = logging.getLogger("SEARCH_ITEMS")
            logger.info("Module SEARCH_ITEMS started")

    def logging_action(name, image):
        if show_img:
            cv.imshow(name, image)
        if img_log:
            cv.imwrite(log_path + name + ".jpg", image)
        if text_log:
            logger.info(repr(name) + " saved on " + repr(log_path + name + ".jpg"))

    items = []

    logging_action("1-source", img)

    img_resize = cv.resize(img, (0, 0), fx=image_scale_factor, fy=image_scale_factor)

    logging_action("2-resize", img_resize)

    gray = cv.cvtColor(img_resize, cv.COLOR_BGR2GRAY)

    logging_action("3-gray", gray)

    gaussian = cv.GaussianBlur(gray, gaussian_kernel, 0)

    logging_action("4-gaussian", gaussian)

    v = np.median(gaussian)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    edged = cv.Canny(gaussian, lower, upper)

    logging_action("5-edged", edged)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, close_kernel)
    closed = cv.morphologyEx(edged, cv.MORPH_CLOSE, kernel)

    logging_action("6-closed", closed)

    contours0, hierarchy = cv.findContours(closed.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    total = 0
    # цикл по контурам
    for cnt in contours0:
        rect = cv.minAreaRect(cnt)  # пытаемся вписать прямоугольник
        area = int(rect[1][0] * rect[1][1])  # вычисление площади
        rect = ((int(rect[0][0] / image_scale_factor), int(rect[0][1] / image_scale_factor)),
                (int(rect[1][0] / image_scale_factor), int(rect[1][1] / image_scale_factor)),
                rect[2])

        box = cv.boxPoints(rect)  # поиск четырех вершин прямоугольника
        box = np.int0(box)  # округление координат
        if area > max_area:
            img_crop = crop_rect(img, rect)

            if text_log:
                logger.info("Object " + repr("item_" + str(total)) + " found: " + repr(rect))
            logging_action("item_" + str(total), img_crop)
            if img_log:
                cv.drawContours(img, [box], 0, (255, 0, 0), 2)

            items.append(Item("item_" + str(total), rect, box, img_crop))
            total = total + 1

    logging_action("7-dist", img)
    if img_log:
        cv.waitKey()
        cv.destroyAllWindows()
    if text_log:
        logger.info("Module SEARCH_ITEMS has been successfully completed")
    return items
