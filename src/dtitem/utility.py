import re
from dtitem.features import Feature


class Image:
    def __init__(self, name, rect, box, img):
        self.name = name
        self.center = rect[0]
        self.img_size = rect[1]
        self.angle = rect[2]
        self.box = box
        self.img = img


class Item(Image):
    def __init__(self, name, rect, box, img, barcode=None, color=None, size=None, cl=None):
        super().__init__(name, rect, box, img)
        if cl is None:
            self.cl = {}
        else:
            self.cl = cl
        self.barcode = barcode
        self.color = color
        self.size = size

    def __str__(self):
        return "Item(name=" + repr(self.name) + ",\n" \
               "     center=" + str(self.center) + ",\n" \
               "     img_size=" + repr(self.img_size) + ",\n" \
               "     angle=" + repr(self.angle) + ",\n" \
               "     box=" + re.sub("[ \n\r]", '', repr(self.box)) + ",\n" \
               "     class=" + repr(self.cl) + ",\n" \
               "     color=" + repr(self.color) + ",\n" \
               "     size=" + repr(self.size) + ",\n" \
               "     barcode=" + str(self.barcode) + ")"

    def __repr__(self):
        return "Item(name=" + repr(self.name) + ",\n" \
               "     center=" + str(self.center) + ",\n" \
               "     size=" + repr(self.size) + ",\n" \
               "     angle=" + repr(self.angle) + ",\n" \
               "     box=" + re.sub("[ \n\r]", '', repr(self.box)) + ",\n" \
               "     class=" + repr(self.cl) + ",\n" \
               "     color=" + repr(self.color) + ",\n" \
               "     size=" + repr(self.size) + ",\n" \
               "     barcode=" + repr(self.barcode) + ")"


class Barcode(Image):
    def __init__(self, code, rect, box, img):
        super().__init__(code, rect, box, img)
        self.code = code

    def __str__(self):
        return "Barcode(code=" + repr(self.code) + ")"

    def __repr__(self):
        return "Barcode(code=" + repr(self.code) + ",\n" \
               "     center=" + str(self.center) + ",\n" \
               "     size=" + repr(self.img_size) + ",\n" \
               "     angle=" + repr(self.angle) + ",\n" \
               "     box=" + re.sub("[ \n\r]", '', repr(self.box)) + ")"


class Category:
    """
    Defines the category to which an object can belong.\n
    Constructor takes a category name and a set of feature.\n
    """
    def __init__(self, name, *features: Feature):
        self.name = name
        self.features = features

    def get_feature(self, cls: type):
        for feature in self.features:
            if type(feature) is cls:
                return feature
        return None

    def __repr__(self):
        return "Category(name=" + repr(self.name) + ")"


class CategoryBase:
    def __init__(self, *categories: Category):
        self.categories = categories

    def add(self, category: Category):
        self.categories.append(category)
