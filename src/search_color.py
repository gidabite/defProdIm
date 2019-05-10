import numpy as np
import random
import os
import logging
import datetime

from dtitem.config import (get_config)


def search_color_item(item, config=None):
    if config is None:
        config = get_config()

    logger = None

    text_log = config["Logging"].getboolean("text_log")
    img_log = config["Logging"].getboolean("img_log")
    config["Logging"]["log_path"] = config["Logging"]["log_path"].format(date_time=str(datetime.datetime.today()))
    log_path = config["Logging"]["log_path"]
    count_samples = config["Color"].getint("count_samples")

    if text_log or img_log:
        if not os.path.exists(log_path + item.name + "/"):
            os.makedirs(log_path + item.name + "/")
        if text_log:
            logger = logging.getLogger("SEARCH_COLOR")
            logger.info("Module SEARCH_COLOR started")

    def logging_action(color):
        if text_log:
            logger.info("The calculated average color:" + str(color))

    height = item.img.shape[0]
    width = item.img.shape[1]
    avg_color = np.zeros(3)

    for i in range(count_samples):
        w = int(random.uniform(0, width))
        h = int(random.uniform(0, height))
        avg_color += item.img[h][w]
    avg_color /= count_samples
    logging_action(avg_color)
    item.color = avg_color.astype(np.int)

    return item
