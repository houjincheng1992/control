# coding=utf-8
import time

from copy import deepcopy

from importlib import import_module
from django.conf import settings

from django.utils.translation import ugettext as _
from rest_framework.response import Response
from rest_framework import status

from console.common.helper import get_module_from_action
from console.common import ConsoleApiView
from console.common.utils import console_response
from console.console.logger import getLogger

from console.apps.records.action_record import record_action_decorator
from console.apps.records.constants import RESOURCES

from .serializers import ManyObjectsValidator


logger = getLogger(__name__)


class Router(ConsoleApiView):
    def get(self, request, *args, **kwargs):
        modules = RESOURCES
        return Response(data=modules, status=status.HTTP_200_OK)

    @record_action_decorator
    def post(self, request, *args, **kwargs):
        req_data = request.data
        validated_data = request.validated_data
        _req_data = deepcopy(req_data)
        if "login_password" in req_data:
            _req_data["login_password"] = "*" * len(_req_data["login_password"])
        logger.info("Get a request: %s" % _req_data)

        # 在操作日志装饰器中已经做过一次校验
        # 校验是否传入了 action、zone、owner这三个必传参数
        # validator = RouterValidator(data=req_data)
        # if not validator.is_valid():
        #     return Response({"code": 1, "msg": validator.errors, "data": {}})

        # 校验action是否符合action校验器的规范
        action = validated_data["action"]
        _module, action, _action, err = get_module_from_action(action)
        if err is not None:
            resp = console_response(code=1, msg=_("The action is not valid"))
            return Response(resp, status=status.HTTP_200_OK)

        # 是否返回多个纪录值，如果是的话则需要校验传递的参数是否符合多传回值的校验规范
        many = validated_data.get("many", False)
        if many:
            many_validator = ManyObjectsValidator(data=req_data)
            if not many_validator.is_valid():
                resp = console_response(code=1, msg=_("many_validator.errors"))
                return Response(resp, status=status.HTTP_200_OK)

        # 尝试导入相应模块的views
        try:
            module = import_module("console.apps.%s.views" % _module, package=["*"])
        except ImportError as exp:
            resp = console_response(code=1, msg=_(exp.message))
            return Response(resp, status=status.HTTP_200_OK)

        # 判断相应的views里面是否实现了相应的action view类
        _view_class = getattr(module, _action, None)
        if _view_class is None:
            resp = console_response(code=1, msg=_("view class was not implemented"))
            return Response(resp, status=status.HTTP_200_OK)

        # 判断传入的owner是否是当前认证用户
        if getattr(request.user, "username", None) != req_data.get("owner") and not settings.DEBUG:
            return Response(console_response(code=1, msg="The owner is not the authenticated user"),
                            status=status.HTTP_200_OK)

        # 注入zone和owner信息到request， 方便调用
        request.zone = req_data.get("zone")
        request.owner = req_data.get("owner")

        # 调用相应模块的views的post方法
        _start = time.time()
        resp = _view_class().post(request, *args, **kwargs)
        _end = time.time()
        logger.info("Get Response: %s, cost:%f" % (resp.data, _end - _start))
        # add action
        resp.data["action"] = validated_data["action"]
        return resp