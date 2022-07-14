# -*- coding: utf-8 -*-
# File     : login.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-14 11:32
# Remarks  :
from tortoise.queryset import Q

from ..models import Login
from ..exceptions import RepositoriesError


class LoginRepository:
    """login repository"""

    def __init__(self):
        """
        装载
        Args:
        """
        pass

    @staticmethod
    async def rep_get_login_by_unique(unique_id):
        try:
            login = await Login.filter(Q(unique_id=unique_id)).prefetch_related("user").first()
            return login
        except Exception as err:
            raise RepositoriesError(
                message=f"Get login exception: {str(err)}", code=400
            )

    @staticmethod
    async def rep_add_login(args):
        """

        Args:
            args:

        Returns:

        """
        try:
            result = await Login.create(**args)
            return result.id
        except Exception as err:
            raise RepositoriesError(
                message=f"Add login exception: {str(err)}", code=400
            )

    @staticmethod
    async def rep_delete_login(_id):
        """
        Args:
            _id:
        Returns:
        """
        try:
            total = await Login.filter(Q(pk=_id)).delete()
            return total
        except Exception as err:
            raise RepositoriesError(
                message=f"Delete login exception: {str(err)}", code=400
            )
