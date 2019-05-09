import numpy as np
import os
import logging
import datetime

from dtitem.config import (get_config)


def search_size_item(item, config=None):
    if config is None:
        config = get_config()

    logger = None

    text_log = config["Logging"].getboolean("text_log")
    img_log = config["Logging"].getboolean("img_log")
    show_img = config["Logging"].getboolean("show_img")
    config["Logging"]["log_path"] = config["Logging"]["log_path"].format(date_time=str(datetime.datetime.today()))
    log_path = config["Logging"]["log_path"]
    scale = config["Size"].getfloat("scale")

    if text_log or img_log:
        if not os.path.exists(log_path + item.name + "/"):
            os.makedirs(log_path + item.name + "/")
        if text_log:
            logger = logging.getLogger("SEARCH_SIZE")
            logger.info("Module SEARCH_SIZE started")

    def logging_action(size):
        if text_log:
            logger.info("The calculated size:" + str(size))

    item.size = np.array(item.img_size)*scale

    logging_action(item.size)

    return item
