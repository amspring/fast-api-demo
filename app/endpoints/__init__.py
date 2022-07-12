# -*- coding: utf-8 -*-
# File     : __init__.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
from fastapi import FastAPI

from ..conf import settings
from . import carousel, user


def register_router(app: FastAPI) -> None:
    """
    注册路由
    Args:
        app: FastAPI app
    Returns:
    """
    app.include_router(carousel.router, prefix=settings.app.prefix)
    app.include_router(user.router, prefix=settings.app.prefix)
