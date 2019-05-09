from dtitem.utility import (Item, CategoryBase, Category)
from dtitem.features import *
from dtitem.config import (get_config)
from typing import List
import numpy as np


def classify_barcode(item: Item, cb: CategoryBase):
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


def classify_color(item: Item, cb: CategoryBase):
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
            k += 1/p
        k = 1/k
        for i in range(probabilities.size):
            probabilities[i] = k/probabilities[i]
    return probabilities


def classify_size(item: Item, cb: CategoryBase):
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


def classify(items: List[Item], cb: CategoryBase, config=None) -> List[Item]:
    if config is None:
        config = get_config()
    search_barcode_enabled = config["Barcode"].getboolean("enabled")
    search_color_enabled = config["Color"].getboolean("enabled")
    search_size_enabled = config["Size"].getboolean("enabled")
    search_neural_enabled = config["Neural"].getboolean("enabled")
    threshold_ration = config["General"].getfloat("threshold_ration")

    for i in range(len(items)):
        count_methods = 0
        if search_barcode_enabled:
            barcode_proximity = classify_barcode(items[i], cb)
            if barcode_proximity.max() != 0:
                items[i].cl = list(zip(cb.categories, barcode_proximity))
                continue
        proximity = np.zeros(len(cb.categories))
        if search_color_enabled:
            count_methods += 1
            proximity += classify_color(items[i], cb)
        max_item = proximity.max()
        max_near = np.delete(proximity, proximity.argmax()).max()
        if max_item/max_near >= threshold_ration:
            items[i].cl = list(zip(cb.categories, proximity.round(3)))
            continue
        if search_size_enabled:
            count_methods += 1
            proximity += classify_size(items[i], cb)
        proximity /= count_methods
        items[i].cl = list(zip(cb.categories, proximity.round(3)))

    return items
