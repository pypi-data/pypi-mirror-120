# -*- coding: utf-8 -*-

import pandas as pd


# 세줄 짜리인데 필요한가?
def 튜플컬럼을_문자열컬럼으로_변환(df):
    tpl_col_li = list(df.columns)
    new_cols = ['_'.join(c) if type(c)==tuple else c for c in tpl_col_li]
    df.columns = new_cols
    return df
#삭제 예정
def 문자열컬럼을_튜플컬럼으로_변환(df):
    str_col_li = list(df.columns)
    str_col_li.remove('_id')
    tpl_col_li = []
    for col in str_col_li:
        tpl = tuple(col.split('_'))
        tpl_col_li.append(tpl)
    return tpl_col_li

def 문자열에서_특수문자를_제거(x):
    특수문자_li = ["[", "]", '"', "'", ",",')','(','-']
    x = str(x)
    x_li = list(x)
    new_x_li = []
    for e in x_li:
        if (e in 특수문자_li) == False:
            new_x_li.append(e)

    x = ''.join(new_x_li)
    return x
