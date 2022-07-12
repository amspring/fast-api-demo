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
from ..schemas import PageMixin, SearchIn, UserAddIn
from ..utils import verify_token

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


@router.post("/user")
@inject
async def f(args: UserAddIn,
            # token: dict = Depends(verify_token),
            service: UserService = Depends(Provide[Container.user_service])):
    """
    添加
    Args:
        args:
        # token:
        service:
    Returns:
    """
    # token 验证
    # user_id = token.get("id")

    result = await service.add_user(args.dict(exclude_none=True))

    return resp_200(data={"id": result})
