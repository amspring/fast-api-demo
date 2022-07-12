# -*- coding: utf-8 -*-
# File     : carousel.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request

from ..resp import resp_200
from ..containers import Container
from ..services import CarouselService
from ..schemas import PageMixin, SearchIn, IdMixin, CarouselAdd, CarouselUpdate
from ..conf import settings

router = APIRouter()


# region ping/version

@router.get("/ping")
async def ping():
    return "PONG"


@router.get("/version")
async def version():
    return settings.app.version


@router.get("/carousels")
@inject
async def f(pagination: PageMixin = Depends(PageMixin),
            args: SearchIn = Depends(SearchIn),
            service: CarouselService = Depends(Provide[Container.carousel_service])):
    """
    列表
    Args:
        pagination:
        args:
        service:
    Returns:
    """
    result = await service.get_carousel_list(pagination, args.dict(exclude_none=True))

    return resp_200(data=result)


@router.get("/carousel/get")
@inject
async def f(args: IdMixin = Depends(IdMixin),
            service: CarouselService = Depends(Provide[Container.carousel_service])):
    """
    详情
    Args:
        args:
        service:
    Returns:
    """
    result = await service.carousel_detail(args.id)

    return resp_200(data=result)


@router.post("/carousel")
@inject
async def f(request: Request,
            args: CarouselAdd,
            service: CarouselService = Depends(Provide[Container.carousel_service])):
    """
    添加
    Args:
        request:
        args:
        service:
    Returns:
    """
    if not args.user_id:
        args.user_id = request.headers.get('request-user-id', 0)

    result = await service.add_carousel(args.dict(exclude_none=True))

    return resp_200(data={"id": result})


@router.put("/carousel/{_id}")
@inject
async def f(_id: int,
            args: CarouselUpdate,
            service: CarouselService = Depends(Provide[Container.carousel_service])):
    """
    修改
    Args:
        _id:
        args:
        service:
    Returns:
    """
    result = await service.update_carousel(_id, args.dict(exclude_none=True))

    return resp_200(data={"update_total": result})


@router.delete("/carousel/{_id}")
@inject
async def f(_id: int,
            service: CarouselService = Depends(Provide[Container.carousel_service])):
    """
    删除
    Args:
        _id:
        service:
    Returns:
    """
    result = await service.delete_carousel(_id)

    return resp_200(data={"delete_total": result})
