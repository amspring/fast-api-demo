# -*- coding: utf-8 -*-
# File     : carousel.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
import urllib.parse
from tortoise.queryset import Q

from ..utils import YesOrNo
from ..models import Carousel
from ..exceptions import RepositoriesError


class CarouselRepository:
    """carousel repository"""

    def __init__(self):
        """
        装载
        Args:
        """
        pass

    @staticmethod
    async def rep_carousel_list(page, per_page, args):
        """
        Args:
            page:
            per_page:
            args:
        Returns:
        """
        try:
            model = Carousel.filter(Q(deleted=YesOrNo.N.value, enabled=YesOrNo.Y.value))

            # 联合查询
            if args.get("username__icontains"):
                model = model.filter(
                    Q(user__username__icontains=urllib.parse.unquote(args.get("username__icontains"))))

            # 总数
            total = await model.count()
            # 分页
            offset = (page - 1) * per_page
            # prefetch_related("user") 关联查询预加载
            results = await model.prefetch_related("user").limit(per_page).offset(offset)

            return results, total
        except Exception as err:
            raise RepositoriesError(
                message=f"Get carousel list exception: {str(err)}", code=400
            )

    @staticmethod
    async def rep_get_carousel(_id):
        """
        Args:
            _id:
        Returns:
        """
        try:
            # prefetch_related("user") 关联查询预加载
            info = await Carousel.filter(Q(pk=_id)).prefetch_related("user").first()
            return info
        except Exception as err:
            raise RepositoriesError(
                message=f"Get carousel detail exception: {str(err)}", code=400
            )

    @staticmethod
    async def rep_add_carousel(args):
        """
        Args:
            args:
        Returns:
        """
        try:
            result = await Carousel.create(**args)
            return result.id
        except Exception as err:
            raise RepositoriesError(
                message=f"Add carousel exception: {str(err)}", code=400
            )

    @staticmethod
    async def rep_update_carousel(_id, args):
        """
        Args:
            _id:
            args:
        Returns:
        """
        try:
            update_total = await Carousel.filter(Q(pk=_id)).update(**args)
            return update_total
        except Exception as err:
            raise RepositoriesError(
                message=f"Update carousel exception: {str(err)}", code=400
            )

    @staticmethod
    async def rep_delete_carousel(_id):
        """
        软删除
        Args:
            _id:
        Returns:
        """
        try:
            delete_total = await Carousel.filter(Q(pk=_id)).update(**{
                "deleted": YesOrNo.Y.value,
            }) if await Carousel.filter(Q(pk=_id) & Q(deleted=YesOrNo.N.value)).exists() else 0

            return delete_total
        except Exception as err:
            raise RepositoriesError(
                message=f"Delete carousel exception: {str(err)}", code=400
            )

    @staticmethod
    async def rep_hard_delete_carousel(_id):
        """
        硬删除
        Args:
            _id:
        Returns:
        """
        try:
            delete_total = await Carousel.filter(Q(pk=_id)).delete() if await Carousel.filter(
                Q(pk=_id) & Q(deleted=YesOrNo.N.value)).exists() else 0

            return delete_total
        except Exception as err:
            raise RepositoriesError(
                message=f"Delete carousel exception: {str(err)}", code=400
            )
