# coding=utf-8
import time
from importlib import import_module
from django.conf import settings

from django.utils.translation import ugettext as _
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from control.control.logger import getLogger

logger = getLogger(__name__)

class Router(APIView):
    def get(self, request, *args, **kwargs):
        modules = RESOURSES
        return Response(data=modules, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        req_data = request.data
        validated_data = request.validated_data
        logger.info("Get a request: %s" % req_data)

        # 校验action是否复合action校验器的规范
        action = validated_data["action"]
        _module, action, _action, err = get_module_from_action(action)
        if err is not None:
            resp = control_response(code=1, msg=_("the action is not valid"))
            return Response(resp, status=status.HTTP_200_OK)

        # 尝试导入相应模块的views
        try:
            module = import_module("control.apps.%s.views" % _module, package=["*"])
        except ImportError as exp:
            resp = control_response(code=1, msg=_(exp.message))
            return Response(resp, status=status.HTTP_200_OK)

        # 判断相应的view是否已经实现了相应的action view 类
        _view_class = getattr(module, _action, None)
        if _view_class is None:
            resp = control_response(code=1, msg=_("view class was not implemented"))
            return Response(resp, status=status.HTTP_200_OK)

        # 调用相应模块的views的post方法
        _start = time.time()
        resp = _view_class().post(request, *args, **kwargs)
        _end = time.time()
        logger.info("Get Response: %s, cost: %f" % (resp.data, _end-_start))
        # add action
        resp.data["action"] = validated_data["action"]
        return resp
