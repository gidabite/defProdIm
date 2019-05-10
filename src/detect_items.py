import os
import logging
import cv2 as cv
import datetime

from dtitem.config import (get_config)
from dtitem.utility import (CategoryBase)
from dtitem.search_items import (search_items)
from dtitem.search_barcode import (search_barcode_item)
from dtitem.search_color import (search_color_item)
from dtitem.search_size import (search_size_item)
from dtitem.classify import (classify)


def detect_items(img_path, cb: CategoryBase, config=None):
    if config is None:
        config = get_config()

    logger = None

    text_log = config["Logging"].getboolean("text_log")
    img_log = config["Logging"].getboolean("img_log")
    config["Logging"]["log_path"] = config["Logging"]["log_path"].format(date_time=str(datetime.datetime.today()))
    log_path = config["Logging"]["log_path"]
    search_barcode_enabled = config["Barcode"].getboolean("enabled")
    search_color_enabled = config["Color"].getboolean("enabled")
    search_size_enabled = config["Size"].getboolean("enabled")
    search_neural_enabled = config["Neural"].getboolean("enabled")

    if text_log or img_log:

        if not os.path.exists(log_path):
            os.makedirs(log_path)
        if text_log:
            logging.basicConfig(filename=log_path + "log",
                                level=logging.INFO,
                                format=u'[%(asctime)s][%(name)12s]# %(message)s',
                                datefmt="%Y-%m-%d %H:%M:%S")
            logger = logging.getLogger("DETECT_ITEMS")

    img = cv.imread(img_path)
    if text_log:
        logger.info("Source image is loaded from " + repr(img_path))
    items = search_items(img, config)
    if text_log:
        logger.info("Module SEARCH_ITEMS found " + str(len(items)) + " objects")
    for item in items:
        if text_log:
            logger.info("Module SEARCH_BARCODE started on " + repr(item.name))

        if search_barcode_enabled:
            item = search_barcode_item(item, config)

        if search_color_enabled:
            item = search_color_item(item, config)

        if search_size_enabled:
            item = search_size_item(item, config)
        item = classify(item, cb)
    if text_log:
        logger.info("Processing the image is complete")
    return items
