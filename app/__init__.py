# -*- coding: utf-8 -*-
# Project  : app
# File     : __init__.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
from fastapi import FastAPI

from .containers import Container
from .endpoints import register_router
from .conf import settings
from .exceptions import register_exception
from .db import register_db


def create_app() -> FastAPI:
    """
    创建app
    Args:

    Returns:

    """
    app = FastAPI(
        debug=settings.app.debug,
        title=settings.app.name,
        description=settings.app.description,
        version=settings.app.version,
    )

    # container
    _register_container(app)

    # routes
    _register_router(app)

    # exception
    _register_exception(app)

    # tortoise
    _register_tortoise(app)

    # consul
    # _register_consul()

    return app


def _register_container(app: FastAPI):
    """
    注册container
    Args:
        app:

    Returns:

    """
    container = Container()
    app.container = container


def _register_router(app: FastAPI) -> None:
    """
    注册路由
    Args:
        app: fast api app

    Returns:

    """
    register_router(app)


def _register_exception(app: FastAPI) -> None:
    """
    注册全局异常
    Args:
        app: fast api
    Returns:
    """
    register_exception(app)


def _register_tortoise(app: FastAPI) -> None:
    """
    注册tortoise
    Args:
        app:

    Returns:

    """
    register_db(app)