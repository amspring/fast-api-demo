# -*- coding: utf-8 -*-
# File     : login.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-14 11:09
# Remarks  :
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from ..resp import resp_200
from ..containers import Container
from ..services import LoginService
from ..schemas import LoginIn, LoginAddIn, PasswordUpdateIn
from ..security import verify_token

router = APIRouter()


@router.post("/login")
@inject
async def f(args: LoginIn,
            service: LoginService = Depends(Provide[Container.login_service])):
    """
    登录验证获取token
    Args:
        args:
        service:
    Returns:
    """

    result = await service.auth_token(args)

    return resp_200(data=result)


@router.post("/login/new")
@inject
async def f(args: LoginAddIn,
            auth: dict = Depends(verify_token),
            service: LoginService = Depends(Provide[Container.login_service])):
    """
    添加登录方式
    Args:
        auth:
        args:
        service:
    Returns:
    """

    result = await service.generate_login(args)

    return resp_200(data=result)


@router.delete("/login")
@inject
async def f(args: LoginIn,
            service: LoginService = Depends(Provide[Container.login_service])):
    """
    登录验证获取token
    Args:
        args:
        service:
    Returns:
    """

    result = await service.auth_token(args)

    return resp_200(data=result)


@router.put("/login/password")
@inject
async def f(args: PasswordUpdateIn,
            auth: dict = Depends(verify_token),
            service: LoginService = Depends(Provide[Container.login_service])):
    """
    修改密码
    Args:
        auth:
        args:
        service:
    Returns:
    """
    result = await service.change_password(args)

    return resp_200(data=result)
