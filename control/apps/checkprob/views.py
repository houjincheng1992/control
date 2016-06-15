# coding=utf-8

from control.control.base import control_code
from control.control.base import control_response

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializer import CheckProbSerializer
from .helper import Router
from control.control.logger import getLogger
from control.control.base import get_path

logger = getLogger(__name__)


class CheckProb(APIView):
    """
    checkProb
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
        validator = CheckProbSerializer(data=req_data)
        logger.info("validator is valid: %s" % validator.is_valid())
        if not validator.is_valid():
            code, msg = control_code(validator)
            logger.error(str(validator.errors))
            return Response(control_response(code=code, msg=msg),
                            status=status.HTTP_200_OK)

        action = validator.validated_data.get("action", "checkprob")
        demodSignal_id = validator.validated_data.get("demodSignal_id", None)


        payload = {
            "demodSignal_id": demodSignal_id,
            "action": action
        }
        logger.info("The main payload is %s" % payload)
        router = Router(payload)
        resp = router.ActionRouter()

        return Response(resp, status=status.HTTP_200_OK)