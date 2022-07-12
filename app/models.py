# -*- coding: utf-8 -*-
# Project  : app
# File     : schemas.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
from tortoise import models, fields
from .utils import YesOrNo


# region mixin models
class IdiMixin(models.Model):
    """主键"""
    id = fields.IntField(generated=True, pk=True, description="标识")

    class Meta:
        abstract = True


class StateMixin(models.Model):
    """状态"""
    enabled = fields.IntEnumField(YesOrNo, default=YesOrNo.Y)
    deleted = fields.IntEnumField(YesOrNo, default=YesOrNo.N)

    class Meta:
        abstract = True


class TimeMixin(models.Model):
    """time stamp mixin"""
    # 创建于
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    # 更新于
    modified_at = fields.DatetimeField(null=True, auto_now=True)

    class Meta:
        abstract = True


class User(IdiMixin, StateMixin, TimeMixin):
    username = fields.CharField(max_length=32, default="", description="用户名")
    avatar = fields.CharField(max_length=255, default="", description="头像")
    password = fields.CharField(max_length=128, default="", description="密码")
    mobile = fields.CharField(max_length=16, null=False, unique=True, description="手机号")

    class Meta:
        table_description = '用户表'
        table = "tb_user"


class Carousel(IdiMixin, StateMixin, TimeMixin):
    url = fields.CharField(max_length=255, null=False, default='', description="链接地址")
    cover = fields.CharField(max_length=255, null=True, default='', description="封面")

    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField("models.User", related_name=False)

    class Meta:
        table_description = '轮播图帧表'
        table = "tb_carousel"
        order = ("-created_at",)

# endregion
