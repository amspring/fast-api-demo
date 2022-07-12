# -*- coding: utf-8 -*-
# File     : carousel.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
from ..repositories import CarouselRepository


class CarouselService:
    """background service"""

    def __init__(self, carousel_repository: CarouselRepository):
        """
        装载
        Args:
            carousel_repository: read repository
        """
        self._repository = carousel_repository

    @staticmethod
    def _carousel(result):
        _result = dict(result)
        _result["username"] = result.user.username if result.user else ""
        return _result

    async def get_carousel_list(self, pagination, args):
        """
        列表
        Args:
            pagination:
            args:
        Returns:
        """

        results, total = await self._repository.get_carousel_list(pagination.page, pagination.per_page, args)
        _result = [self._carousel(result) for result in results]

        return {
            "list": _result,
            "total": total
        }

    async def carousel_detail(self, _id):
        """
        详情
        Args:
            _id:
        Returns:
        """
        result = await self._repository.carousel_detail(_id)

        if not result:
            return {}

        return self._carousel(result)

    async def add_carousel(self, args):
        """
        添加
        Args:
            args:
        Returns:
        """
        result = await self._repository.carousel_add(args)

        return result

    async def update_carousel(self, _id, args):
        """
        编辑
        Args:
            _id:
            args:
        Returns:
        """
        result = await self._repository.carousel_update(_id, args)

        return result

    async def delete_carousel(self, _id):
        """
        删除
        Args:
            _id:
        Returns:
        """
        result = await self._repository.carousel_delete(_id)

        return result
