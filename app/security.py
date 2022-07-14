# -*- coding: utf-8 -*-
# Project  : app
# File     : security.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
import jwt
import random
import string
import time

from fastapi import Request
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256

from .conf import settings
from .exceptions import AuthTokenMissing, AuthTokenCorrupted, AuthTokenExpired


def generate_salt(length=6):
    """密盐
    Args:
        length:
    Returns:
    """
    return "".join(random.sample(string.ascii_letters + string.digits, length))


def generate_password_hash(password, salt) -> str:
    """加密
    Args:
        password: 密码
        salt: 密盐
    Returns:
    """
    return pbkdf2_sha256.hash(password, rounds=12000, salt=salt.encode("utf-8"))


def check_password_hash(password_hash, password_plain) -> bool:
    """检查密码
    Args:
        password_hash: 加密后的密码
        password_plain: 明文
    Returns:
        True or False
    """
    return pbkdf2_sha256.verify(password_plain, password_hash)


def expire_time_format(expire):
    """过期时间转换
    Args:
        expire:
    Returns:
    """
    expire_time = (datetime.now() + timedelta(seconds=expire)).strftime("%Y-%m-%d %H:%M:%S")
    _dt = time.strptime(expire_time, "%Y-%m-%d %H:%M:%S")

    return time.mktime(_dt), expire_time


def time_stamp_format(times):
    """时间戳转日期
    Args:
        times:
    Returns:
    """
    _time = time.localtime(times)

    return time.strftime("%Y-%m-%d %H:%M:%S", _time)


async def verify_token(request: Request):
    """
    token验证
    Args:
        request:
    Returns:

    """
    return await decode_access_token(get_header_token(request))


def get_header_token(request: Request):
    """
    拦截token
    Args:
        request:
    Returns:
    """
    authorization = request.headers.get('authorization', "Bearer ")
    return authorization.replace(f'Bearer ', '')


async def generate_access_token(data: dict, expire: int = None):
    """加密, 生成token
    Args:
        data: 数据
        expire: 过期时间,单位秒
    Returns:
    """
    if not expire:
        expire, time_now = expire_time_format(settings.auth.D_2)

    token_data = {
        'id': data['id'],
        'role': data['role'],
        'exp': expire,
    }

    return jwt.encode(token_data, settings.auth.secret_key, algorithm=settings.auth.algorithm)


async def generate_refresh_token(data: dict, expire: int = None):
    """加密传输的数据
    Args:
        data:
        expire:
    Returns:
    """
    if not expire:
        expire, time_now = expire_time_format(settings.auth.D_2)

    token_data = {
        'id': data['id'],
        'exp': expire,
    }

    return jwt.encode(token_data, settings.auth.secret_key, algorithm=settings.auth.algorithm)


async def decode_access_token(token: str = None):
    """
    Args:
        token:
    Returns:
    """
    if not token:
        raise AuthTokenMissing()

    try:
        payload = jwt.decode(token, settings.auth.secret_key, algorithms=settings.auth.algorithm)
        return payload
    except jwt.exceptions.ExpiredSignatureError:
        raise AuthTokenExpired()
    except jwt.exceptions.DecodeError:
        raise AuthTokenCorrupted()
