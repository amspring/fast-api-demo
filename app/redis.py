# -*- coding: utf-8 -*-
# File     : redis.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-14 11:14
# Remarks  :
import aioredis
from typing import AsyncIterator
from aioredis import ConnectionPool, Redis

from .conf import settings


async def init_redis() -> AsyncIterator[Redis]:
    pool = ConnectionPool.from_url(url=settings.redis, decode_responses=True)
    connect = aioredis.Redis(connection_pool=pool)
    yield connect
    await connect.close()
