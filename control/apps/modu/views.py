# coding=utf-8
from django.shortcuts import render

from control.control.base import control_code
from control.control.base import control_response
from control.control.base import user_temp

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializer import CreateSignalSerializer
from .sub_view import Router

# from control.control.base import get_path
from control.control.logger import getLogger

logger = getLogger(__name__)

from .models import SignalModel
# Create your views here.


class CreateSignal(APIView):
    """
    创建信号
    """
    # action = "CreateSignal"

    def post(self, request, *args, **kwargs):
        req_data = request.data
        logger.info(req_data)
        # logger.info(get_path.MATLAB_FILE_PATH)
        # logger.info(get_path.CELERY_PATH)
        # logger.info(get_path.CURRENT_PATH)
        # logger.info("filename is %s" % SignalModel.get_signal_by_id("signal-h7aiwz4v").filename)
        validator = CreateSignalSerializer(data=req_data)
        logger.info("validator is valid: %s" % validator.is_valid())
        if not validator.is_valid():
            code, msg = control_code(validator)
            logger.error(str(validator.errors))
            return Response(control_response(code=code, msg=msg),
                            status=status.HTTP_200_OK)

        filename = validator.validated_data.get("filename", None)
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

        payload = {
            # "action": self.action,
            "filename": filename,
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
            "signal_id": signal_id
        }

        logger.info("The main payload is %s" % payload)
        route = Router(payload)
        resp = route.Actionrouter()
        return Response(resp, status=status.HTTP_200_OK)