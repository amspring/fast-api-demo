# -*- coding: utf-8 -*-
# Project  : app
# File     : resp.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
import datetime
from typing import Union
from fastapi import status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder


def escaped_datetime(obj: datetime.datetime, mapping=None) -> str:
    """
    格式化时间
    """
    s = "%Y-%m-%d %H:%M:%S"
    return obj.strftime(s)


def resp_200(*, code=200, data: Union[str, list, dict, int, float] = None, message="Success") -> Response:
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder({
                            "code": code,
                            "message": message,
                            "data": data,
                        },
                            custom_encoder={datetime.datetime: escaped_datetime}
                        ))


def resp_500(*, data: Union[str, list, dict, int, float] = None, message="Internal Server Error") -> Response:
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=jsonable_encoder({
                            "code": 500,
                            "message": message,
                            "data": data,
                        }))
