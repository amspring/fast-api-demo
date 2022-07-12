# -*- coding: utf-8 -*-
# File     : user.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 13:57
# Remarks  :
from datetime import datetime
from tortoise.queryset import Q

from ..utils import YesOrNo
from ..models import User
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
    async def get_user_list(page, per_page, args):
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
    async def user_add(args):
        """
        Args:
            args:
        Returns:
        """
        try:
            result = await User.create(**args)
            return result.id
        except Exception as err:
            raise RepositoriesError(
                message=f"Add user exception: {str(err)}", code=400
            )
