from abc import (ABC, abstractmethod)
import numpy as np


class Feature(ABC):
    """
    Defines the base class of the feature that objects can have.\n
    Is an abstract class. Use feature classes inherited from this class
    """

    @abstractmethod
    def proximity(self, item):
        pass


class BarcodeFeature(Feature):
    """
    Defines the feature responsible for the presence of the barcode\n
    Constructor takes a barcode as an argument
    """

    def __init__(self, barcode: str):
        self.barcode = barcode

    def proximity(self, item):
        return self.barcode == item.barcode.code


class ColorFeature(Feature):
    """
    Defines the feature corresponding to the average color of the object.\n
    Constructor takes one color as the only argument in the format: [r, g, b]
    """

    def __init__(self, r, g, b):
        self.color = np.array([r, g, b])

    def proximity(self, item):
        return np.linalg.norm(self.color - item.color)


class SizeFeature(Feature):
    """
    Defines the property that determines the size of the object\n
    Constructor takes the size of the object as the only argument in the format: [height, width]
    """

    def __init__(self, width, height):
        self.size = np.array([width, height])

    def proximity(self, item):
        """

        :param item:
        :return:
        """
        return min(
            np.linalg.norm(self.size - item.size),
            np.linalg.norm(self.size - item.size[::-1])
        )
