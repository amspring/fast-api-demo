# -*- coding: utf-8 -*-
# File     : login.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-14 11:11
# Remarks  :
from aioredis import Redis

from ..exceptions import ServiceError
from ..repositories import UserRepository, LoginRepository
from ..security import generate_password_hash, generate_salt, generate_access_token, expire_time_format
from ..conf import settings


class LoginService:
    """user service"""

    def __init__(self, redis_client: Redis, login_repository: LoginRepository, user_repository: UserRepository):
        """装载
        Args:
            redis_client:
            user_repository: UserRepository
        """
        self._redis = redis_client
        self._login_repository = login_repository
        self._user_repository = user_repository

    async def set_cache(self, key: str, maps: dict, expire: int = None):
        """
        缓存Hash数据
        Args:
            key:
            maps:
            expire: 单位 s
        Returns:
        """
        await self._redis.hmset(key, maps)

        # 设置过期时间
        if expire:
            await self._redis.expire(key, expire)

    async def get_cache(self, key: str):
        """
        获取缓存数据
        Args:
            key:
        Returns:
        """
        return await self._redis.hgetall(key)

    async def auth_token(self, args):
        """ token 认证
        Args:
            args:
        Returns:
        """
        login = await self._login_repository.rep_get_login_by_unique(unique_id=args.unique_id)

        if not login:
            raise ServiceError(
                message=f"The login does not exist: unique_id={args.unique_id}", code=404
            )

        if generate_password_hash(args.password, login.user.salt) != login.user.password:
            raise ServiceError(
                message=f"The supplied password is incorrect", code=400
            )

        expire, expire_time = expire_time_format(settings.auth.D_2)
        access_token = await generate_access_token(data={
            "id": login.user.id,
            "role": 0
        }, expire=expire)

        await self.set_cache(
            access_token,
            {"id": login.user.id, "role": 0, "username": login.user.username, "avatar": login.user.avatar}
        )

        return {
            "access_token": access_token,
            "token_type": settings.auth.token_type,
            "expire": expire_time,
            "id": login.user.id,
            "username": login.user.username,
            "avatar": login.user.avatar
        }

    async def generate_login(self, args):
        """添加登录方式
        Args:
            args:
        Returns:
        """
        login = await self._login_repository.rep_get_login_by_unique(unique_id=args.unique_id)
        if login:
            raise ServiceError(
                message=f"The login account already exists: unique_id={args.unique_id}", code=402
            )

        user = await self._user_repository.rep_get_user(args.user_id)
        if not user:
            raise ServiceError(
                message=f"The user does not exist: user_id={args.user_id}", code=404
            )

        if generate_password_hash(args.password, user.salt) != user.password:
            raise ServiceError(
                message=f"The supplied password is incorrect", code=400
            )

        result = await self._login_repository.rep_add_login({"user_id": args.user_id, "unique_id": args.unique_id})

        return result

    async def change_password(self, args):
        """修改密码
        Args:
            args:
        Returns:
        """
        if args.password != args.conf_password:
            raise ServiceError(
                message=f"Confirm that the two passwords are the same", code=400
            )

        salt = generate_salt()
        data = {
            "salt": salt,
            "password": generate_password_hash(args.password, salt)
        }

        result = await self._user_repository.rep_update_user(args.user_id, data)

        return result
