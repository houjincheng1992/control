# coding=utf-8

from control.control.base import control_response

from .tasks import Demode_single_ant
from .tasks import Demode_double_ant
from .tasks import Demode_four_ant

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
        logger.info("payload is %s" % payload)
        if not isinstance(ant_type, list):
            ant_type = [ant_type]

        for key_ant_type in ant_type:

            if key_ant_type == "single_ant":
                sub_payload = {
                    "signal_id": signal_id,
                    "protocol": protocol
                }
                logger.info("The sub_payload is %s" % sub_payload)
                Demode_single_ant.apply_async([sub_payload])
                logger.info("The sub_payload is %s" % sub_payload)

            if key_ant_type == "douoble_ant":
                sub_payload = {
                    "signal_id": signal_id,
                    "protocol": protocol
                }
                Demode_double_ant.apply_async([sub_payload])

            if key_ant_type == "four_ant":
                sub_payload = {
                    "signal_id": signal_id,
                    "protocol": protocol
                }
                Demode_four_ant.apply_async([sub_payload])
        return control_response(code=0, msg="Demod is running!")
