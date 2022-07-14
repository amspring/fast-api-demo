# -*- coding: utf-8 -*-
# File     : user.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 13:57
# Remarks  :
from tortoise.queryset import Q
from tortoise.transactions import in_transaction

from ..utils import YesOrNo
from ..models import User, Login
from ..exceptions import RepositoriesError


class UserRepository:
    """user repository"""

    def __init__(self):
        """
        装载
        Args:
        """
        pass

    @staticmethod
    async def rep_user_list(page, per_page, args):
        """
        Args:
            page:
            per_page:
            args:
        Returns:
        """
        try:
            model = User.filter(Q(deleted=YesOrNo.N.value)).filter(**args)

            # 总数
            total = await model.count()
            # 分页
            offset = (page - 1) * per_page
            results = await model.limit(per_page).offset(offset)

            return results, total
        except Exception as err:
            raise RepositoriesError(
                message=f"Get User list exception: {str(err)}", code=400
            )

    @staticmethod
    async def rep_get_user(user_id):
        """
        Args:
            user_id:
        Returns:
        """
        try:
            user = await User.filter(Q(pk=user_id)).first()
            return user
        except Exception as err:
            raise RepositoriesError(
                message=f"Get User exception: {str(err)}", code=400
            )

    @staticmethod
    async def rep_add_user(args):
        """
        Args:
            args:
        Returns:
        """
        async with in_transaction("default") as conn:
            try:
                # 用户添加
                user = await User.create(**args, using_db=conn)

                # 关联登录
                await Login.create(user=user, unique_id=args.get("mobile"), using_db=conn)

                return user.id
            except Exception as err:
                raise RepositoriesError(
                    message=f"Add user exception: {str(err)}", code=400
                )

    @staticmethod
    async def rep_update_user(_id, args):
        """
        Args:
            _id:
            args:
        Returns:
        """
        try:
            update_total = await User.filter(Q(pk=_id)).update(**args)
            return update_total
        except Exception as err:
            raise RepositoriesError(
                message=f"Update user exception: {str(err)}", code=400
            )

    @staticmethod
    async def rep_delete_user(_id):
        """
        Args:
            _id:
        Returns:
        """
        try:
            total = await User.filter(Q(pk=_id)).delete()
            return total
        except Exception as err:
            raise RepositoriesError(
                message=f"Delete User exception: {str(err)}", code=400
            )

    @staticmethod
    async def rep_check_user(_id):
        """
        Args:
            _id:
        Returns:
        """
        try:
            flag = await User.filter(Q(pk=_id)).exists()
            return flag
        except Exception as err:
            raise RepositoriesError(
                message=f"Check User exist exception: {str(err)}", code=400
            )