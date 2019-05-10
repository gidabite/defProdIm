from dtitem.features import *
from dtitem.config import (get_config)
import numpy as np


def classify_barcode(item, cb):
    probabilities = np.zeros(len(cb.categories))
    i = 0
    count = 0
    for category in cb.categories:
        feature = category.get_feature(BarcodeFeature)
        if feature is None:
            raise Exception("BarcodeFeature not found")
        proximity = feature.proximity(item)
        if proximity:
            probabilities[i] = 1.0
            count += 1
        i += 1
    if count != 0:
        probabilities /= count
    return probabilities


def classify_color(item, cb):
    probabilities = np.zeros(len(cb.categories))
    i = 0
    used_proximity = []
    for category in cb.categories:
        feature = category.get_feature(ColorFeature)
        if feature is None:
            raise Exception("ColorFeature not found")
        probabilities[i] = feature.proximity(item) + 0.1
        used_proximity.append(probabilities[i])
        i += 1
    if len(used_proximity) > 0:
        probabilities /= min(used_proximity)
        k = 0
        for p in probabilities:
            k += 1 / p
        k = 1 / k
        for i in range(probabilities.size):
            probabilities[i] = k / probabilities[i]
    return probabilities


def classify_size(item, cb):
    probabilities = np.zeros(len(cb.categories))
    i = 0
    used_proximity = []
    for category in cb.categories:
        feature = category.get_feature(SizeFeature)
        if feature is None:
            raise Exception("SizeFeature not found")
        probabilities[i] = feature.proximity(item) + 0.1
        used_proximity.append(probabilities[i])
        i += 1
    if len(used_proximity) > 0:
        probabilities /= min(used_proximity)
        k = 0
        for p in probabilities:
            k += 1 / p
        k = 1 / k
        for i in range(probabilities.size):
            probabilities[i] = k / probabilities[i]
    return probabilities


def classify(item, cb, config=None):
    if config is None:
        config = get_config()
    search_barcode_enabled = config["Barcode"].getboolean("enabled")
    search_color_enabled = config["Color"].getboolean("enabled")
    search_size_enabled = config["Size"].getboolean("enabled")
    search_neural_enabled = config["Neural"].getboolean("enabled")
    threshold_ration = config["General"].getfloat("threshold_ration")

    count_methods = 0
    if search_barcode_enabled:
        barcode_proximity = classify_barcode(item, cb)
        if barcode_proximity.max() != 0:
            item.cl = sorted(list(zip(cb.categories, barcode_proximity)), key=lambda x: x[1], reverse=True)
            return item
    proximity = np.zeros(len(cb.categories))
    if search_color_enabled:
        count_methods += 1
        proximity += classify_color(item, cb)
    max_item = proximity.max()
    max_near = np.delete(proximity, proximity.argmax()).max()
    if max_item / max_near >= threshold_ration:
        item.cl = sorted(list(zip(cb.categories, proximity.round(3))), key=lambda x: x[1], reverse=True)
        return item
    if search_size_enabled:
        count_methods += 1
        proximity += classify_size(items[i], cb)
    proximity /= count_methods
    item.cl = sorted(list(zip(cb.categories, proximity.round(3))), key=lambda x: x[1], reverse=True)
    return item
