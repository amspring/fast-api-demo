# -*- coding: utf-8 -*-
# File     : db.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .conf import settings

TORTOISE_ORM = {
    'connections': {'default': settings.mariadb},
    'apps': {
        'models': {
            'models': [
                'aerich.models',
                'app.models'
            ],
            'default_connection': 'default'
        },
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}


def register_db(app: FastAPI) -> None:
    """
    注册tortoise
    Args:
        app:
    Returns:
    """
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=settings.app.debug,
        add_exception_handlers=settings.app.debug
    )
