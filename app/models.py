# -*- coding: utf-8 -*-
# Project  : app
# File     : schemas.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
from tortoise import models, fields

from .utils import YesOrNo, Gender


# region mixin models
class IdiMixin(models.Model):
    """主键"""
    id = fields.IntField(generated=True, pk=True, description="主键")

    class Meta:
        abstract = True


class StateMixin(models.Model):
    """状态"""
    enabled = fields.IntEnumField(YesOrNo, default=YesOrNo.Y, description="0: 禁用, 1: 启用")
    deleted = fields.IntEnumField(YesOrNo, default=YesOrNo.N, description="0: 未删除, 1: 已删除")

    class Meta:
        abstract = True


class TimeMixin(models.Model):
    """time stamp mixin"""
    created_at = fields.DatetimeField(null=True, auto_now_add=True, description="创建于")
    modified_at = fields.DatetimeField(null=True, auto_now=True, description="更新于")

    class Meta:
        abstract = True


class UserMixin(models.Model):
    """关联用户, 一对一"""
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField("models.User", related_name=False)

    class Meta:
        abstract = True


class User(IdiMixin, StateMixin, TimeMixin):
    username = fields.CharField(max_length=32, default="", description="用户名")
    avatar = fields.CharField(max_length=255, default="", description="头像")
    mobile = fields.CharField(max_length=16, null=False, unique=True, description="手机号")
    salt = fields.CharField(max_length=12, null=False, description="密盐")
    password = fields.CharField(max_length=128, null=False, description="密码")
    email = fields.CharField(max_length=32, null=False, unique=True, default='')
    gender = fields.IntEnumField(Gender,  default=Gender.SECRET)

    class Meta:
        table_description = '用户表'
        table = "tb_user"


class Login(IdiMixin, StateMixin, TimeMixin, UserMixin):
    unique_id = fields.CharField(max_length=32, null=False, unique=True, description="登录账户")

    class Meta:
        table_description = '登录表'
        table = "tb_login"


class Carousel(IdiMixin, StateMixin, TimeMixin, UserMixin):
    url = fields.CharField(max_length=255, null=False, default='', description="链接地址")
    cover = fields.CharField(max_length=255, null=True, default='', description="封面")

    class Meta:
        table_description = '轮播图表'
        table = "tb_carousel"
        order = ("-created_at",)

# endregion
