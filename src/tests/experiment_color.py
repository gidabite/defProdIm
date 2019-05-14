import cv2 as cv
import numpy as np
import dtitem
import timeit
import matplotlib.pyplot as plt
import random
import math

fn = './samples/multi_6.jpg'
config = dtitem.get_config()

items = dtitem.search_items(cv.imread(fn))
item = items[1]

count = 1000
count_samples = 100
times = np.zeros(count)
means = np.zeros(count_samples)
sko = np.zeros(count_samples)
height = item.img.shape[0]
width = item.img.shape[1]
for i in range(count_samples):
    print(i)
    colors = []
    color_mean = np.zeros(3)
    for j in range(count):

        avg_color = np.zeros(3)
        d = (i + 1) * 10
        start = timeit.default_timer()
        for z in range(d):
            w = int(random.uniform(0, width))
            h = int(random.uniform(0, height))
            avg_color += item.img[h][w]
        avg_color /= d
        color_mean += avg_color
        times[j] = (timeit.default_timer() - start)*1000
        colors.append(avg_color)
    np_colors = np.asarray(colors)
    color_mean /= count
    m = 0
    for j in range(count):
        np_colors[j] -= color_mean
        m += np.linalg.norm(np_colors[j])
    m /= count
    m = math.sqrt(m)
    means[i] = round(times.mean(), ndigits=2)
    sko[i] = m

plt.plot([(i + 1) * 10 for i in range(count_samples)], means)
#plt.plot([i for i in range(count)], [mean for i in range(count)], "r")
plt.xlabel("Count")
plt.ylabel("time, ms")
#plt.title("search_barcode_item, mean = %2.2f ms" % mean)
plt.show()
plt.plot([(i + 1) * 10 for i in range(count_samples)], sko, "r")
#plt.plot([i for i in range(count)], [mean for i in range(count)], "r")
plt.xlabel("Count")
plt.ylabel("SKO")
#plt.title("search_barcode_item, mean = %2.2f ms" % mean)
plt.show()
