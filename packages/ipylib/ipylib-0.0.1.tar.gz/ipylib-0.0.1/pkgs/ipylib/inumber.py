# -*- coding: utf-8 -*-
import re
import pandas as pd
import numpy as np

from idebug import *
from ipylib.base import BaseClass



class StrNumberParser(object):
    # StringType-Number 문자형-숫자

    def __init__(self, s, sosujeom='.'):
        if isinstance(s, str):
            self._s = s.strip()
            self._sosujeom = sosujeom
            # 정수 부분 천단위 구분포멧
            self._fmt = ',' if self._sosujeom == '.' else '.'
            self.__NumSystem = '스페인식' if self._sosujeom == ',' else '국제표준'

            # PartGubun('파싱')
            p_fmt = '\.' if self._fmt == '.' else self._fmt
            p_jeom = '\.' if self._sosujeom == '.' else self._sosujeom
            s = self._s
            # 앞에 '0' 안붙이고 소수점이하 숫자일 경우 예외처리
            if re.search(f'^{p_jeom}', s) is not None:
                s = s.zfill(len(s)+1)
            # 공통 파싱
            m = re.search(f'([\+-])*([{p_fmt}|\d]+|[\d]+)({p_jeom})*(\d+)*', s)
            # print(m.groups())
            pm, i, jeom, sosu = m[1], m[2], m[3], m[4]

            # PartGubun('컴포넌트 결정')
            self._sign = 1 if pm in [None,'+'] else -1
            self._int = int(i.replace(self._fmt, ''))
            # 소수점을 '.'으로 표준화
            jeom = '.' if jeom == ',' else jeom
            sosu = f'{jeom}{sosu}' if jeom != None and sosu != None else None
            self._sosu = .0 if sosu is None else float(sosu)
            self._is_int = True if sosu is None else False
            v = self._int + self._sosu
            v = int(v) if self._is_int else float(v)
            self.v = self._sign * v
        elif isinstance(s, int) or isinstance(s, float):
            self.v = s
        else:
            logger.info(f'문자형숫자를 입력해라. s --> {s} {type(s)}')

    def __str__(self):
        if hasattr(self, 'v'):
            return str(self.v).format("{:,}")


def StrNumber(s, sosujeom='.'):
    return StrNumberParser(s, sosujeom).v


class Percent(BaseClass):
    # 순수숫자를 입력하면 퍼센트숫자가 아니다.
    # 퍼센트가 순수숫자로 변환완료된 수라고 가정한다
    _err_msg = "사용예시: ('0.23' -> 0.23%) (0.23 -> 23%)"

    def __init__(self, v, prec=2, sosujeom='.'):
        # Percent Precision: 퍼센트 소수점이하 자릿수
        self._p_prec = prec
        # Number Precision: 퍼센트를 숫자로 변환시 소수점이하 자릿수
        self._n_prec = prec + 2
        self._sosujeom = sosujeom
        if isinstance(v, str):
            sn = StrNumberParser(v, self._sosujeom)
            self.pct = round(sn.v, self._p_prec)
            self.num = round(self.pct / 100, self._n_prec)
            self.str = self._build_str(sn)
        elif isinstance(v, float) or isinstance(v, int):
            self.num = round(float(v), self._n_prec)
            self.pct = round(self.num * 100, self._p_prec)
            sn = StrNumberParser(str(self.pct), self._sosujeom)
            self.str = self._build_str(sn)
        else:
            logger.critical(f"{self} | {self._err_msg} | v: {v} {type(v)}")

    def _sosu_str(self, sn):
        # 소수점이하 수를 문자열로 변경하고, 소수점으로 분리한 후, 소수점이하 자릿수를 조정한다
        prec = str(sn._sosu).split('.')[1]
        return prec.ljust(self._p_prec, '0')

    def _build_str(self, sn):
        return str(sn._int) + self._sosujeom + self._sosu_str(sn) + '%'


# ============================================================
# 삭제 대기 중 --> StrNumber 로 통합하라
def parse_numStr(s, pct=False):
    if isinstance(s, str):
        s, n = re.subn('%$', '', s.strip())
        is_percent = False if n == 0 else True

        s = s.replace(',', '')
        m = re.search('([\+-])*(\d+)(\.\d+)*', s)
        if m.group(3) == None:
            v = int(m.group(2))
        else:
            v = int(m.group(2)) + float(m.group(3))
        if m.group(1) != None:
            sign = int(f"{m.group(1)}1")
            v *= sign

        return v / 100 if is_percent or pct else v
    elif isinstance(s, int):
        return s / 100 if pct else s
    elif isinstance(s, float):
        return s / 100 if pct else s
    else:
        return s

"""개발중"""
def NumStrParser(s, type='int', pct=False, ndigits=None):
    n = parse_numStr(s, pct)
    n = abs(n) if type == 'abs' else n
    n = n if isinstance(ndigits, int) else round(n, ndigits)
    return n
    
# ============================================================
# 예전 함수들. 필요한 것만 골라내라

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
