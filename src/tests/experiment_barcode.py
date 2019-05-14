import cv2 as cv
import numpy as np
import dtitem
import timeit
import matplotlib.pyplot as plt
from pyzbar.pyzbar import (decode, ZBarSymbol)

fn = './samples/multi_6.jpg'
config = dtitem.get_config()

items = dtitem.search_items(cv.imread(fn))
item = items[1]

count = 10000
times = np.zeros(count)
for i in range(count):
    start = timeit.default_timer()
    barcode = decode(item.img, [ZBarSymbol.EAN13])
    times[i] = (timeit.default_timer() - start)*1000

mean = round(times.mean(), ndigits=2)

plt.plot([i for i in range(count)], times)
plt.plot([i for i in range(count)], [mean for i in range(count)], "r")
plt.xlabel("Count")
plt.ylabel("time, ms")
plt.title("search_barcode_item, mean = %2.2f ms" % mean)
plt.show()
plt.savefig('books_read.png')
