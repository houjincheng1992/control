# coding=utf-8

from control.control.base import control_code
from control.control.base import control_response

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializer import DemodSignalSerializer
from .helper import Router
from control.control.logger import getLogger
from control.control.base import get_path

logger = getLogger(__name__)


class DemodSignal(APIView):
    """
    Demode signals
    """
    def post(self, request, *args, **kwargs):
        """
        接受post请求数据并处理
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        req_data = request.data
        logger.info(req_data)
        validator = DemodSignalSerializer(data=req_data)
        logger.info("validator is valid: %s" % validator.is_valid())
        if not validator.is_valid():
            code, msg = control_code(validator)
            logger.error(str(validator.errors))
            return Response(control_response(code=code, msg=msg),
                            status=status.HTTP_200_OK)

        signal_id = validator.validated_data.get("signal_id", None)
        ant_type = validator.validated_data.get("ant_type", "single_ant")
        protocol = validator.validated_data.get("protocol", "SOTDMA")
        sync_type = validator.validated_data.get("sync_type", "DEFAULT")

        payload = {
            "signal_id": signal_id,
            "ant_type": ant_type,
            "protocol": protocol,
            "sync_type": sync_type
        }
        logger.info("The main payload is %s" % payload)
        router = Router(payload)
        resp = router.Ant_select()

        return Response(resp, status=status.HTTP_200_OK)