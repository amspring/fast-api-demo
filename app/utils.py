# -*- coding: utf-8 -*-
# Project  : app
# File     : utils.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
import base64
import datetime

from typing import Union
from fastapi import Request
from enum import IntEnum, unique
from tortoise.queryset import QuerySet


@unique
class Gender(IntEnum):
    """性别"""
    # 女
    FEMALE = 0
    # 男
    MALE = 1
    # 保密
    SECRET = 2


@unique
class YesOrNo(IntEnum):
    """是否可用"""

    Y = 1
    N = 0


async def verify_token(request: Request):
    """authorization验证 """
    authorization = request.headers.get('authorization', "Bearer ")
    token = authorization.replace(f'Bearer ', '')
    if not token:
        return {"msg": "缺少token认证"}

    temp = token.split(".")
    if len(temp) != 3:
        return {"msg": "token认证错误"}

    return decode_base64(temp[1])


def decode_base64(param):
    """
    Args:
        param: token 中间一段的值
    Returns:
    """
    missing_padding = 4 - len(param) % 4
    if missing_padding:
        param = bytes(param, encoding='utf8')
        param += b'=' * missing_padding
        param = eval(str(base64.b64decode(param), encoding="utf-8"))
    return param


async def row_to_dict(row,
                      select: Union[list] = None,
                      unselect: Union[list] = None,
                      queryset: bool = None) -> Union[dict]:
    """
    QuerySet 格式化时间, 2021-06-16T03:50:18+00:00-> 2021-06-16 03:50:18
    依赖关联信息转成dict, QuerySet -> dict
    """
    temp = {}
    select = select if select else []
    unselect = unselect if unselect else []

    if not row:
        return temp

    _table = dict()
    for column in row:
        if unselect:
            if column[0] not in unselect:
                _table[column[0]] = column[1]
        elif select and not unselect:
            if column[0] in select:
                _table[column[0]] = column[1]
        else:
            _table[column[0]] = column[1]

    for key, value in _table.items():
        if type(value) == datetime:
            temp[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        elif type(value) == QuerySet:
            if queryset:
                _value = await value
                q_val = _value.__dict__ if _value else {}
                temp[key] = q_val
        else:
            temp[key] = value

    return temp
