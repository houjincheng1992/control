# coding=utf-8

from django.conf import settings

from control.control.base import control_response
from control.control.err_msg import DemodErrorCode

from .models import DemodModel
from .tasks import Demod_single_ant
from .tasks import Demod_double_ant
from .tasks import Demod_four_ant

from control.control.logger import getLogger

logger = getLogger(__name__)


class Router():
    def __init__(self, payload):
        self.payload = payload

    def Ant_select(self):
        """
        选择解调的天线类型
        :return:
        """
        payload = self.payload
        ant_type = payload.get("ant_type")
        signal_id = payload.get("signal_id")
        protocol = payload.get("protocol")
        sync_type = payload.get("sync_type")
        logger.info("payload is %s" % payload)
        demod_model, error = DemodModel.objects.create(signal_id=signal_id,
                                                       ant_type=ant_type,
                                                       protocol=protocol,
                                                       sync_type=sync_type)
        if not demod_model:
            return control_response(code=DemodErrorCode.DEMOD_SAVE_FAILED, msg=error)

        if not isinstance(ant_type, list):
            ant_type = [ant_type]

        for key_ant_type in ant_type:

            if key_ant_type == "single_ant":
                sub_payload = {
                    "signal_id": signal_id,
                    "protocol": protocol,
                    "sync_type": sync_type,
                    "action": ant_type
                }
                logger.info("The sub_payload is %s" % sub_payload)
                if settings.IF_RUN_MATLAB == 'True':
                    Demod_single_ant.apply_async([sub_payload])

            if key_ant_type == "douoble_ant":
                sub_payload = {
                    "signal_id": signal_id,
                    "protocol": protocol,
                    "sync_type": sync_type,
                    "action": ant_type
                }
                if settings.IF_RUN_MATLAB == 'True':
                    Demod_double_ant.apply_async([sub_payload])

            if key_ant_type == "four_ant":
                sub_payload = {
                    "signal_id": signal_id,
                    "protocol": protocol,
                    "sync_type": sync_type,
                    "action": ant_type
                }
                if settings.IF_RUN_MATLAB == 'True':
                    Demod_four_ant.apply_async([sub_payload])
        return control_response(code=0, msg="Demod is running!")
