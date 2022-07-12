# -*- coding: utf-8 -*-
# Project  : app
# File     : security.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
from passlib.hash import pbkdf2_sha256


def generate_password_hash(password) -> str:
    """加密
    Args:
        password: 密码

    Returns:

    """
    return pbkdf2_sha256.hash(password, rounds=12000, salt_size=6)


def check_password_hash(password_hash, password_plain) -> bool:
    """检查密码
    Args:
        password_hash: 加密后的密码
        password_plain: 明文
    Returns:
        True or False
    """
    return pbkdf2_sha256.verify(password_plain, password_hash)
