# -*- coding: utf-8 -*-
# File     : db.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
from .conf import settings
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

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
        generate_schemas=False,
        add_exception_handlers=True,
    )
