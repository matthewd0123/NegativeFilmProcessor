# Reader for raw negative film scans from digital cameras or scanners. 
# File format can be in any raw format or .TIFF
# Raw format will be converted to .TIFF first

import rawpy
import imageio
import time
import matplotlib.pyplot as plt
from pathlib import Path
import cv2 as cv


def raw2Tiff(raw, saveTiff = True, tiffName = "Raw_convert.tiff"):
    """
    Read raw image and convert to .tiff file.
    Return the RGB infomation in an array.
    """
    print("* Converting raw image to TIFF file ...     *")
    st = time.time()
    colorArray = raw.postprocess()
    if saveTiff:
        imageio.imsave(tiffName, colorArray)
        print("* Converted TIFF file saved                 *")
    print("  ", "%.2f" % (time.time()-st), " seconds used for conversion")

    return colorArray


def rawReader(path,):
    if path.endswith((".tiff",".tif")):
        print("* Reading the nagative image ...            *")
        colorArray = plt.imread(path)
    else:
        raw = rawpy.imread(path)
        colorArray = raw2Tiff(raw, True, Path(path).with_suffix(".tiff"))

    return colorArray


def histogramRGB(colorArray,):
    """
    View the histogram of an image. 
    In log scale by default.
    """
    RGB = ('r','g','b')
    plt.rcParams["figure.figsize"] = (3,3)
    for i,col in enumerate(RGB):
        histr = cv.calcHist([colorArray],[i],None,[256],[0,256])
        plt.plot(histr,color = col)
        plt.xlim([0,256])
    # plt.yscale('log')
    plt.show()
