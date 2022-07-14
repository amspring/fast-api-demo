# -*- coding: utf-8 -*-
# Project  : app
# File     : req.py
# Author   : csc
# Version  : v1.0
# Email    : csc@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
from typing import Optional

from pydantic import BaseModel, Field, constr, conint

"""Field
default: （位置参数）字段的默认值。由于Field替换了字段的默认值，因此第一个参数可用于设置默认值。使用省略号 ( …) 表示该字段为必填项。
alias: 字段的别名
gt: 对于数值 ( int, float, ), 向 JSON SchemaDecimal添加“大于”的验证和注释exclusiveMinimum
ge: 对于数值，这将添加“大于或等于”的验证和minimumJSON 模式的注释
lt: 对于数值，这会为exclusiveMaximumJSON Schema添加“小于”的验证和注释
le: 对于数值，这将添加“小于或等于”的验证和maximumJSON 模式的注释
......
"""


class PageMixin(BaseModel):
    """分页"""
    page: conint(gt=0) = 1
    per_page: conint(gt=0) = 20


class IdMixin(BaseModel):
    id: int = None


class EnableMixin(BaseModel):
    enabled: int = None


class SearchIn(BaseModel):
    """搜索 """
    # orm模糊查询: __icontains, 字段别名: alias
    username__icontains: Optional[str] = Field(default=None, alias="name")


class CarouselAddIn(BaseModel):
    url: str
    cover: str
    user_id: int


class CarouselUpdateIn(BaseModel):
    url: str = None


class UserAddIn(BaseModel):
    username: str
    mobile: Optional[str] = Field(min_length=11, max_length=11, default='')
    password: constr(min_length=8, max_length=32)


class UserUpdateIn(BaseModel):
    username: str = None
    avatar: str = None
    email: str = None
    gender: int = None


class PasswordUpdateIn(BaseModel):
    password: str
    conf_password: str
    user_id: int


class LoginIn(BaseModel):
    password: str
    unique_id: str = Field(default=..., alias="login")


class LoginAddIn(LoginIn):
    user_id: int
