# -*- coding: utf-8 -*-
# File     : user.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 13:54
# Remarks  :

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from ..resp import resp_200
from ..containers import Container
from ..services import UserService
from ..schemas import PageMixin, SearchIn, UserAddIn, UserUpdateIn
from ..security import verify_token, get_header_token

router = APIRouter()


@router.get("/users")
@inject
async def f(pagination: PageMixin = Depends(PageMixin),
            args: SearchIn = Depends(SearchIn),
            service: UserService = Depends(Provide[Container.user_service])):
    """
    列表
    Args:
        pagination:
        args:
        service:
    Returns:
    """
    result = await service.get_user_list(pagination, args.dict(exclude_none=True))

    return resp_200(data=result)


@router.get("/user/{_id}")
@inject
async def f(_id: int,
            service: UserService = Depends(Provide[Container.user_service])):
    """
    详情
    Args:
        _id:
        service:
    Returns:
    """
    result = await service.get_user(_id)

    return resp_200(data=result)


@router.post("/user")
@inject
async def f(args: UserAddIn,
            auth: dict = Depends(verify_token),
            service: UserService = Depends(Provide[Container.user_service])):
    """
    添加
    Args:
        args:
        auth:
        service:
    Returns:
    """
    # token 验证
    # user_id = token.get("id")

    result = await service.add_user(args.dict(exclude_none=True))

    return resp_200(data={"id": result})


@router.put("/user/{_id}")
@inject
async def f(_id: int,
            args: UserUpdateIn,
            auth: dict = Depends(verify_token),
            service: UserService = Depends(Provide[Container.user_service])):
    """
    修改
    Args:
        auth:
        _id:
        args:
        service:
    Returns:
    """
    result = await service.update_user(_id, args.dict(exclude_none=True))

    return resp_200(data={"update_total": result})


@router.delete("/user/{_id}")
@inject
async def f(_id: int,
            auth: dict = Depends(verify_token),
            service: UserService = Depends(Provide[Container.user_service])):
    """
    删除
    Args:
        auth:
        _id:
        service:
    Returns:
    """
    result = await service.delete_user(_id)

    return resp_200(data={"delete_total": result})


@router.get("/myself")
@inject
async def f(auth: dict = Depends(verify_token),
            token: str = Depends(get_header_token),
            service: UserService = Depends(Provide[Container.user_service])):
    """
    用户详情
    Args:
        auth:
        token:
        service:
    Returns:
    """
    result = await service.myself(auth.get("id"))

    return resp_200(data=result)
