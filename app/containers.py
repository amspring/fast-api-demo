# -*- coding: utf-8 -*-
# Project  : app
# File     : containers.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 11:51
# Remarks  :
from dependency_injector import containers, providers

from .redis import init_redis
from .services import CarouselService, UserService, LoginService
from .repositories import CarouselRepository, UserRepository, LoginRepository


class Container(containers.DeclarativeContainer):
    """di container"""
    wiring_config = containers.WiringConfiguration(packages=[".endpoints"])

    config = providers.Configuration()

    _redis_client = providers.Resource(init_redis)

    # 用户
    _user_repository = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService, user_repository=_user_repository)

    # 轮播
    _carousel_repository = providers.Factory(CarouselRepository)
    carousel_service = providers.Factory(CarouselService, carousel_repository=_carousel_repository)

    # 登录
    _login_repository = providers.Factory(LoginRepository)
    login_service = providers.Factory(LoginService, redis_client=_redis_client, login_repository=_login_repository,
                                      user_repository=_user_repository)
