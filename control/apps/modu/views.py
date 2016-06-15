# coding=utf-8
from django.contrib.auth.admin import User
from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from control.control.base import control_code
from control.control.base import control_response
from control.control.base import user_temp

from .serializer import CreateSignalSerializer
from .serializer import DescribeSignalSerializer
from .serializer import DeleteSignalSerializer
from .sub_view import Router

from control.control.logger import getLogger
logger = getLogger(__name__)

from .models import SignalModel
# Create your views here.


class CreateSignal(APIView):
    """
    创建信号
    """
    # action = "CreateSignal"
    # def get(self, request, *args, **kwargs):
    #     """
    #     get 方式发送数据
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     req_data = request.data
    #     logger.info(req_data)
    #     user_id = self.request.Get.get("user_id")
    #     record_signal = SignalModel.signal_get_record()
    #     return record_signal

    def post(self, request, *args, **kwargs):
        req_data = request.data
        logger.info(req_data)
        validator = CreateSignalSerializer(data=req_data)
        logger.info("validator is valid: %s" % validator.is_valid())
        if not validator.is_valid():
            code, msg = control_code(validator)
            return Response(control_response(code=code, msg=msg),
                            status=status.HTTP_200_OK)

        name_signal = validator.validated_data.get("name_signal", None)
        packagenum = validator.validated_data.get("packagenum", 1)
        action_all = validator.validated_data.get("action_all", True)
        action = validator.validated_data.get("action", None)
        lon = validator.validated_data.get("lon", 102.0)
        lat = validator.validated_data.get("lat", 31.8029)
        height = validator.validated_data.get("height", 600)
        vesnum = validator.validated_data.get("vesnum", 500)
        obtime = validator.validated_data.get("obtime", 60)
        ant_pitch = validator.validated_data.get("ant_pitch", 0)
        ant_azimuth = validator.validated_data.get("ant_azimuth", 0)
        ant_type = validator.validated_data.get("ant_type", "yagi")
        channel_tpye = validator.validated_data.get("channel_type", "free space loss")
        protocol = validator.validated_data.get("protocol", "SOTDMA")
        snr = validator.validated_data.get("snr", 0)
        distri_mode = validator.validated_data.get("distri_mode", "random")
        distri_id = validator.validated_data.get("distri_id", None)
        partable_id = validator.validated_data.get("partable_id", None)
        timetable_id = validator.validated_data.get("timetable_id", None)
        aisdata_id = validator.validated_data.get("aisdata_id", None)
        signal_id = validator.validated_data.get("signal_id", None)
        owner = user_temp()

        # 默认参数 暂未提供接口
        transInterval = 12

        payload = {
            # "action": self.action,
            "name_signal": name_signal,
            "packagenum": packagenum,
            "action_all": action_all,
            "action": action,
            "owner": owner,
            "lon": lon,
            "lat": lat,
            "height": height,
            "vesnum": vesnum,
            "obtime": obtime,
            "ant_pitch": ant_pitch,
            "ant_azimuth": ant_azimuth,
            "ant_type": ant_type,
            "channel_type": channel_tpye,
            "protocol": protocol,
            "snr": snr,
            "distri_mode": distri_mode,
            "distri_id": distri_id,
            "partable_id": partable_id,
            "timetable_id": timetable_id,
            "aisdata_id": aisdata_id,
            "signal_id": signal_id,
            "transInterval": transInterval
        }
        logger.info("The main payload is %s" % payload)
        route = Router(payload)
        resp = route.CreateSignalRouter()
        return Response(resp, status=status.HTTP_200_OK)


class DescribeSignal(APIView):
    """
    查询信号信息
    """
    def post(self, request, *args, **kwargs):
        req_data = parProcess(request.data)
        logger.info("payload is %s" % req_data)
        validator = DescribeSignalSerializer(data=req_data)
        logger.info("validator valid is %s" % validator.is_valid())
        if not validator.is_valid():
            code, msg = control_code(validator)
            return Response(control_response(code=code, msg=msg),
                            status=status.HTTP_200_OK)

        action = validator.validated_data.get("action", "describe")
        signal_id = validator.validated_data.get("signal_id", None)
        payload = {
            "action": action,
            "signal_id": signal_id
        }

        route = Router(payload)
        resp = route.DescribeSignalRouter()
        logger.info("the return is %s" % resp)
        return Response(resp, status=status.HTTP_200_OK)


class DeleteSiganl(APIView):
    """
    删除信号信息
    """
    def post(self, request, *args, **kwargs):
        req_data = request.data
        logger.info("request data is %s" % req_data)
        validator = DeleteSignalSerializer(req_data)
        logger.info("validator valid is %s" % validator.is_valid())
        if not validator.is_valid():
            code, msg = control_code(validator)
            return Response(control_response(code=code, msg=msg),
                            status=status.HTTP_200_OK)

        action = validator.validated_data.get("action", "delete")
        signal_id = validator.validated_data.get("signal_id", None)
        payload = {
            "action": action,
            "signal_id": signal_id
        }
        route = Router(payload=payload)
        resp = route.DeleteSignalRouter()
        return Response(resp, status=status.HTTP_200_OK)


def parProcess(payload):
    """
    数据验证前的数据处理
    :param payload:
    :return:
    """
    distri_id = payload.get("distri_id")
    partable_id = payload.get("partable_id")
    timetable_id = payload.get("timetable_id")
    aisdata_id = payload.get("aisdata_id")
    signal_id = payload.get("signal_id")
    logger.info("signal_id is %s" % signal_id)
    if distri_id:
        if not isinstance(distri_id, list):
            distri_id = [distri_id]
    if partable_id:
        if not isinstance(partable_id, list):
            partable_id = [partable_id]
    if timetable_id:
        if not isinstance(timetable_id, list):
            timetable_id = [timetable_id]
    if aisdata_id:
        if not isinstance(aisdata_id, list):
            aisdata_id = [aisdata_id]
    if signal_id:
        if not isinstance(signal_id, list):
            signal_id = [signal_id]
    payload.update(
        {
            "distri_id": distri_id,
            "partable_id": partable_id,
            "timetable_id": timetable_id,
            "aisdata_id": aisdata_id,
            "signal_id": signal_id
        }
    )
    logger.info(signal_id)
    return payload
