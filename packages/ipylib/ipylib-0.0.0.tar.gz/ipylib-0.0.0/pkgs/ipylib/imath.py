"""
relative change | 증가율, 증감률, 상승율
https://en.wikipedia.org/wiki/Relative_change_and_difference
x2 - x1
_______
  x1


rate (Rate of change) |
https://en.wikipedia.org/wiki/Rate_(mathematics)
f(a+h) - f(a)
_____________
       h
h는 주로 time 인 경우가 많다.
An instantaneous rate of change is equivalent to a derivative.


구성비『統計』 the component[distribution] ratio.
"""


import numpy as np
import inspect

import idebug as dbg



def fraction(numerator, denominator):
    try:
        numerator = float(numerator)
        denominator = float(denominator)
        if denominator == float(0):
            if numerator == float(0):
                return float(0)
            elif numerator > float(0):
                return np.inf
            else:
                return -1*np.inf
        else:
            return numerator/denominator
    except Exception as e:
        dbg.exception(locals(), f"{__name__}.{inspect.stack()[0][3]}")


def relative_change(x1, x2):
    if (x1 != np.nan) and (x2 != np.nan):
        return fraction(x2-x1, abs(x1))
    else:
        return np.nan


def dist_ratio(xlist):
    try:
        print(xlist)
        xs = 0
        for x in xlist:
            xs += x

        rpt_list= []
        for x in xlist:
            rv = fraction(x, xs)
            rpt_list.append(round(rv, 2))
        return rpt_list
    except Exception as e:
        dbg.exception(locals(), f"{__name__}.{inspect.stack()[0][3]}")
