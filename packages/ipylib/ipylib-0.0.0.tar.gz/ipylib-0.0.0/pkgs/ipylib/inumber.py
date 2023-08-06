

import pandas as pd
import numpy as np


def convert_numberstr(numstr):
    if isinstance(numstr, str):
        numstr = numstr.lstrip().rstrip()
        numstr = numstr.replace(',', '')
        if len(numstr) is 0:
            return np.nan
        else:
            if '.' in numstr:
                return float(numstr)
            else:
                return int(numstr)
    else:
        return numstr


def 숫자단위_변경(df, 컬럼_승수_dic):
    df1 = df.copy()
    승수명칭_dic = {4:'_만', 8:'_억', 12:'_조', 16:'_경'}
    for col in 컬럼_승수_dic:
        승수 = 컬럼_승수_dic[col]
        df1[col] = df1[col].apply(lambda x: x/pow(10, 승수))
        #df1 = df1.rename( columns={col: col+승수명칭_dic[승수]} )
    return df1


def 숫자단위_변경대상의_컬럼_승수_dic(df, 제외컬럼_li):
    cols = list(df.columns)
    for e in 제외컬럼_li:
        cols.remove(e)

    컬럼_승수_dic = {}
    for c in cols:
        컬럼_승수_dic[c] = 8
    return 컬럼_승수_dic


def convert_datasize_unit(val, type='count'):
    """데이터크기 단위 변환."""
    KiB = pow(2,10)
    MiB = pow(2,20)
    GiB = pow(2,30)
    TiB = pow(2,40)
    K = pow(10,3)
    M = pow(10,6)
    G = pow(10,9)
    T = pow(10,12)

    if type == 'count':
        if val < K:
            unit = 'decimal'
        elif K <= val < M:
            val = val / K
            unit = 'K'
        elif M <= val < G:
            val = val / M
            unit = 'M'
        elif G <= val < T:
            val = val / G
            unit = 'G'
        else:
            val =  val / T
            unit = 'T'

    elif type == 'byte':
        if val < KiB:
            unit = 'B'
        elif KiB <= val < MiB:
            val = val / KiB
            unit = 'KiB'
        elif MiB <= val < GiB:
            val = val / MiB
            unit = 'MiB'
        elif GiB <= val < TiB:
            val = val / GiB
            unit = 'GiB'
        else:
            val =  val / TiB
            unit = 'TiB'
    else: print('\n 다른 환산 단위는 또 뭐냐\n')

    return (val, unit)


def convert_timeunit(seconds):
    sec = 1
    msec = sec / 1000
    min = sec * 60
    hour = min * 60

    t = seconds
    if t < sec:
        unit = 'msec'
        t = t / msec
    elif sec <= t <= min:
        unit = 'secs'
    elif min < t <= hour:
        unit = 'mins'
        t = t / min
    else:
        unit = 'hrs'
        t = t / hour

    return round(t, 1), unit


def translate_num_to_korean(n):
    if n < pow(10,4):
        unit = ''
    else:
        for i in range(1,10,1):
            n = n/pow(10,4)
            if n < pow(10,4):
                break
        if i is 1:
            unit = '만'
        elif i is 2:
            unit = '억'
        elif i is 3:
            unit = '조'
        elif i is 4:
            unit = '경'
        else:
            print("\n 경 이상의 단위는 다룰 필요가 없다.")
    return f"{round(n,1)}{unit}"
