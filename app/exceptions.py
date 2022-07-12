# -*- coding: utf-8 -*-
# Project  : app
# File     : exceptions.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-07-12 10:25
# Remarks  :
import traceback
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, ValidationError

from .resp import resp_200, resp_500
from .logger import logger


class AuthTokenMissing(Exception):
    def __init__(self, message: str = "缺失token验证.", code: int = 401):
        self.message = message
        self.code = code


class ServiceError(Exception):
    def __init__(self, message: str = "Http请求异常", code: int = 400):
        self.message = message
        self.code = code


class RepositoriesError(Exception):
    def __init__(self, message: str = "数据库请求异常", code: int = 400):
        self.message = message
        self.code = code


def register_exception(app: FastAPI) -> None:
    """
    注册全局异常
    Args:
        app: fast api

    Returns:

    """

    @app.exception_handler(ServiceError)
    async def query_params_exception_handler(request: Request, exc: ServiceError):
        """
        内部查询操作时，其他参数异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"参数查询异常\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return resp_200(message=exc.message, code=exc.code)

    @app.exception_handler(RepositoriesError)
    async def repositories_exception_handler(request: Request, exc: RepositoriesError):
        """
        内部操作数据库时异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"内部操作数据库时异常\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return resp_200(message=exc.message, code=exc.code)

    @app.exception_handler(AuthTokenMissing)
    async def auth_token_miss_exception_handler(request: Request, exc: AuthTokenMissing):
        """
        token丢失错误
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"token 缺失错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return resp_200(message=exc.message, code=exc.code)

    @app.exception_handler(ValidationError)
    async def inner_validation_exception_handler(request: Request, exc: ValidationError):
        """
        内部参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"内部参数验证错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return resp_200(message=exc.errors())

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        请求参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"请求参数格式错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return resp_200(message='; '.join([f"{e['loc'][1]}: {e['msg']}" for e in exc.errors()]))

    # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        全局所有异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"全局异常\n{request.method}URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return resp_500()
