# coding=utf-8

from django.conf import settings

from control.control.base import control_response
from control.control.err_msg import CheckProbErrorCode

from .models import CheckProbModel
from .tasks import CheckProb


from control.control.logger import getLogger

logger = getLogger(__name__)

class Router():
    """
    选择不同的action
    """
    def __init__(self, payload):
        self.payload = payload

    def ActionRouter(self):
        payload = self.payload
        action = payload.get("action", None)
        demodSignal_id = payload.get("demodsignal_id", None)

        checkprob_model, error = CheckProbModel(demodSignal_id=demodSignal_id)
        if not checkprob_model:
            return control_response(code=CheckProbErrorCode.CHEKPROB_SAVE_FAILED, msg = error)

        if action == "checkprob":
            sub_payload = {
                "demodSignal_id": demodSignal_id,
                "action": action
            }
            if settings.IF_RUN_MATLAB == 'True':
                CheckProb.apply_async([sub_payload])
        return control_response(code=0, msg="checkprob is running!")
