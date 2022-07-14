# -*- coding: utf-8 -*-
# Project  : app
# File     : __init__.py.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
from .carousel import CarouselRepository
from .user import UserRepository
from .login import LoginRepository

__all__ = ["CarouselRepository", "UserRepository", "LoginRepository"]
