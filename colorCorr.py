import numpy as np
import pandas
from scipy.optimize import curve_fit
import cv2 as cv
import matplotlib.pyplot as plt
import splines
import reader


def poly(x,orderLi):
    y = (x ** 3) * orderLi[0] + (x ** 2) * orderLi[1] + x * orderLi[2] + orderLi[3]

    return y


def FilmCharaCurve(exp,OrderLi,maxExp,minExp):
    Den = poly(exp, OrderLi)
    DenMin = poly(minExp, OrderLi)
    DenMax = poly(maxExp, OrderLi)
    # stretch linearly
    DenRescaled = (Den - DenMin) / (DenMax - DenMin) * 255

    return DenRescaled


def inverseFilmCharaCurve(OrderLi,maxExp,minExp,color):
    # inputting Density as RGB value to find out the exposure (log).
    DenRescaled = FilmCharaCurve(np.linspace(minExp, maxExp, 256),OrderLi,maxExp,minExp)
    res = splines.CatmullRom(np.linspace(0, 255, 256), DenRescaled)
    plt.plot(DenRescaled,np.linspace(0, 255, 256),color)
    # create LUT from curve
    LUT = np.uint8(res.evaluate(range(0,256)))
    plt.savefig("invCurve.pdf")

    return LUT


def corrColor(colorChannel,LUT):
    imgdtype = colorChannel.dtype
    print(np.maximum(colorChannel,0))
    colorChannelCorr = cv.LUT(colorChannel,LUT)

    return colorChannelCorr


def corrImage(colorArray,curveParamFile, WBTolperc = 0.5):
    b,g,r = cv.split(colorArray)
    curveParam = pandas.read_csv(curveParamFile,delimiter="\t") 
    maxExp = list(curveParam['maxExp'])[0]
    minExp = list(curveParam['minExp'])[0]
    rLUT = inverseFilmCharaCurve(list(curveParam['R']),maxExp,minExp,'r')
    rCorr = corrColor(r,rLUT)
    gLUT = inverseFilmCharaCurve(list(curveParam['G']),maxExp,minExp,'g')
    gCorr = corrColor(g,rLUT)
    bLUT = inverseFilmCharaCurve(list(curveParam['B']),maxExp,minExp,'b')
    bCorr = corrColor(b,rLUT)
    channelLi = [rCorr, gCorr, bCorr]
    # Auto white balance assuming "grey world".
    for i in range(3):
        channelLi[i] = whiteBalance(channelLi[i],WBTolperc)
    imgCorr = cv.merge(channelLi) # in reverse order.

    return imgCorr


def whiteBalance(colorChannel, perc = 0.5):
    mi, ma = (np.percentile(colorChannel, perc), np.percentile(colorChannel,100.0-perc))
    channelBalanced = np.uint8(np.clip((colorChannel-mi)*255.0/(ma-mi), 0, 255))

    return channelBalanced


