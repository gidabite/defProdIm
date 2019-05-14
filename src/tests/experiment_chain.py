import cv2 as cv
import numpy as np
import dtitem
from ast import literal_eval as make_tuple
import timeit
import matplotlib.pyplot as plt

fn = './samples/multi_4.jpg'
config = dtitem.get_config()

image_scale_factor = config["SearchItem"].getfloat("image_scale_factor")
gaussian_kernel = make_tuple(config["SearchItem"]["gaussian_kernel"])
sigma = config["SearchItem"].getfloat("sigma")
close_kernel = make_tuple(config["SearchItem"]["close_kernel"])
max_area = make_tuple(config["SearchItem"]["max_area"])
img_resize = cv.resize(cv.imread(fn), (0, 0), fx=0.1, fy=0.1)
gray = cv.cvtColor(img_resize, cv.COLOR_BGR2GRAY)
v = np.median(gray)
lower = int(max(0, (1.0 - sigma) * v))
upper = int(min(255, (1.0 + sigma) * v))
edged = cv.Canny(gray, lower, upper)
kernel = cv.getStructuringElement(cv.MORPH_RECT, close_kernel)
closed = cv.morphologyEx(edged, cv.MORPH_CLOSE, kernel)

count = 10000
times = np.zeros(count)
for i in range(count):
    start = timeit.default_timer()
    contours0, hierarchy = cv.findContours(closed.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_KCOS)
    for cnt in contours0:
        rect = cv.minAreaRect(cnt)  # пытаемся вписать прямоугольник
    times[i] = (timeit.default_timer() - start)*1000

mean = round(times.mean(), ndigits=2)

plt.plot([i for i in range(count)], times)
plt.plot([i for i in range(count)], [mean for i in range(count)], "r")
plt.xlabel("Count")
plt.ylabel("time, ms")
plt.title("CHAIN_APPROX_TC89_KCOS, mean = %2.2f ms" % mean)
plt.show()
plt.savefig('books_read.png')
