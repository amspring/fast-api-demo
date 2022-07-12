# -*- coding: utf-8 -*-
# Project  : app
# File     : containers.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 11:51
# Remarks  :
from dependency_injector import containers, providers

from .services import CarouselService, UserService
from .repositories import CarouselRepository, UserRepository


class Container(containers.DeclarativeContainer):
    """di container"""
    wiring_config = containers.WiringConfiguration(packages=[".endpoints"])

    config = providers.Configuration()

    # 用户
    _user_repository = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService, user_repository=_user_repository)

    # 轮播
    _carousel_repository = providers.Factory(CarouselRepository)
    carousel_service = providers.Factory(CarouselService, carousel_repository=_carousel_repository)
