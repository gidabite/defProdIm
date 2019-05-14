#!/usr/bin/env python3

import dtitem


def main():
    # fn = './samples/snickers_1.jpg'
    fn = './samples/multi_6.jpg'

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

    detected = dtitem.detect_items(fn, cb)
    print(*detected, sep="\n")


if __name__ == "__main__":
    main()
