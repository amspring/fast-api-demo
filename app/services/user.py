# -*- coding: utf-8 -*-
# File     : user.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 13:56
# Remarks  :
from ..repositories import UserRepository
from ..security import generate_password_hash
from ..utils import row_to_dict


class UserService:
    """user service"""

    def __init__(self, user_repository: UserRepository):
        """
        装载
        Args:
            user_repository: read repository
        """
        self._repository = user_repository

    async def get_user_list(self, pagination, args):
        """
        列表
        Args:
            pagination:
            args:
        Returns:
        """
        results, total = await self._repository.get_user_list(pagination.page, pagination.per_page, args)

        return {
            "list": [await row_to_dict(result, unselect=["password", "deleted"]) for result in results],
            "total": total
        }

    async def add_user(self, args):
        """
        添加
        Args:
            args:
        Returns:
        """
        if args.get("password"):
            args["password"] = generate_password_hash(args.get("password"))

        result = await self._repository.user_add(args)

        return result
