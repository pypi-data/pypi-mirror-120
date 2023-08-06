# -*- coding: utf-8 -*-
from idebug import *
from ipylib.inumber import parse_numStr


def ValueDtypeParser(v, dtype, ndigits=4):
    try:
        if dtype == 'int':
            return parse_numStr(v)
        elif dtype == 'int_abs':
            return abs(parse_numStr(v))
        elif dtype == 'float':
            return round(parse_numStr(v), ndigits)
        elif dtype == 'pct':
            return round(parse_numStr(v, True), ndigits)
        elif dtype in ['date','time','dt','datetime']:
            return DatetimeParser(v)
        elif dtype == 'str':
            return v
    except Exception as e:
        logger.exception(f"파싱 에러가 발생하면, 입력된 값을 그대로 반환한다. {locals()}")
        return v
