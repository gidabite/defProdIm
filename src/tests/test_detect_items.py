from unittest import TestCase
import dtitem
import cv2 as cv
import pandas
import numpy as np
import matplotlib.pyplot as plt
import timeit


class TestDetect_items(TestCase):
    def test_detect_items(self):
        fn = '../samples/multi_6.jpg'
        c1 = dtitem.Category("SNICKERS SUPER",
                             dtitem.BarcodeFeature("5000159455367"),
                             dtitem.ColorFeature(88, 92, 107),
                             dtitem.SizeFeature(18.2, 4.5))
        c2 = dtitem.Category("KITKAT",
                             dtitem.BarcodeFeature("4606272034963"),
                             dtitem.ColorFeature(91, 92, 134),
                             dtitem.SizeFeature(14, 4))
        c3 = dtitem.Category("KITKAT BIG",
                             dtitem.BarcodeFeature("4606272035465"),
                             dtitem.ColorFeature(98, 101, 136),
                             dtitem.SizeFeature(18, 4))
        c4 = dtitem.Category("MARS MAX",
                             dtitem.BarcodeFeature("4607065001490"),
                             dtitem.ColorFeature(102, 116, 127),
                             dtitem.SizeFeature(18.5, 4.5))
        c5 = dtitem.Category("BOUNTY",
                             dtitem.BarcodeFeature("4011100977624"),
                             dtitem.ColorFeature(131, 129, 126),
                             dtitem.SizeFeature(16, 4))
        c6 = dtitem.Category("TWIX",
                             dtitem.BarcodeFeature("4011100977952"),
                             dtitem.ColorFeature(52, 75, 111),
                             dtitem.SizeFeature(16, 8))
        c7 = dtitem.Category("TWIX BIG",
                             dtitem.BarcodeFeature("5000159390729"),
                             dtitem.ColorFeature(75, 97, 131),
                             dtitem.SizeFeature(18.5, 8))

        cb = dtitem.CategoryBase(c1, c2, c3, c4, c5, c6, c7)

        count = 100
        p = np.zeros(count)
        times = np.zeros(count)
        items = dtitem.search_items(cv.imread(fn))
        item = items[2]
        for i in range(count):
            start = timeit.default_timer()
            item = dtitem.search_color_item(item)
            item = dtitem.classify(item, cb)
            times[i] = (timeit.default_timer() - start)*1000
            p[i] = item.cl[0][1]
            self.assertEqual(item.cl[0][0].name, 'BOUNTY')
        p_plot = pandas.Series(p)
        times_plot = pandas.Series(times)
        p_plot.plot.hist(grid=True, bins=20, rwidth=0.9,
                    color='#607c8e').axvline(p.mean(), color="r")

        plt.title('Probability')
        plt.xlabel('Probability')
        plt.ylabel('Count')
        plt.grid(axis='y', alpha=0.75)
        plt.show()

        times_plot.plot.hist(grid=True, bins=20, rwidth=0.9,
                        color='#607c8e').axvline(times.mean(), color="r")

        plt.title('Time')
        plt.xlabel('Time')
        plt.ylabel('Count')
        plt.grid(axis='y', alpha=0.75)
        plt.show()
        x = 4
