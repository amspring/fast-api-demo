# -*- coding: utf-8 -*-
# File     : user.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 13:56
# Remarks  :
from ..utils import row_to_dict
from ..exceptions import ServiceError
from ..repositories import UserRepository
from ..security import generate_password_hash, generate_salt


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
        users, total = await self._repository.rep_user_list(pagination.page, pagination.per_page, args)

        return {
            "list": [await row_to_dict(user, unselect=["password", "salt", "deleted"]) for user in users],
            "total": total
        }

    async def get_user(self, _id):
        """

        Args:
            _id:
        Returns:
        """
        user = await self._repository.rep_get_user(_id)

        return await row_to_dict(user, unselect=["password", "salt", "deleted"])

    async def add_user(self, args):
        """
        添加
        Args:
            args:
        Returns:
        """
        salt = generate_salt()
        args["salt"] = salt
        args["password"] = generate_password_hash(args.get("password"), salt)

        result = await self._repository.rep_add_user(args)

        return result

    async def update_user(self, _id, args):
        """
        编辑
        Args:
            _id:
            args:
        Returns:
        """
        if not await self._repository.rep_check_user(_id):
            raise ServiceError(
                message=f"The user does not exist", code=404
            )

        result = await self._repository.rep_update_user(_id, args)

        return result

    async def delete_user(self, _id):
        """
        删除用户
        Args:
            _id:
        Returns:
        """
        if not await self._repository.rep_check_user(_id):
            raise ServiceError(
                message=f"The user does not exist", code=404
            )

        return await self._repository.rep_delete_user(_id)

    async def myself(self, user_id):
        """
        token个人详情
        Args:
            user_id:
        Returns:
        """
        user = await self._repository.rep_get_user(user_id)
        data = await row_to_dict(user, unselect=["password", "salt", "deleted"])
        # code here you business

        return data
