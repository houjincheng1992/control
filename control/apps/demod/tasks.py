# coding=utf-8

import os
import matlab.engine

from celery import shared_task

from control.control.base import get_path
from control.control.logger import getLogger

logger = getLogger(__name__)


matlab_path = get_path.MATLAB_FILE_PATH
celery_path = get_path.CELERY_PATH

@shared_task()
def Demode_single_ant(payload):
    """
    单天线解调
    :param payload: 解调所需参数
    :return:
    """
    signal_id = payload.get("signal_id", None)
    protocol = payload.get("protocol", None)

    os.chdir(matlab_path)
    eng = matlab.engine.start_matlab()
    try:
        logger.info("start matlab single_ant demode")
        eng.demod(signal_id, protocol)
        eng.quit()
        os.chdir(celery_path)
        return True
    except Exception as exp:
        logger.error("single_ant demode error: %s" % str(exp))
        eng.quit()
        os.chdir(celery_path)
        return False

@shared_task()
def Demode_double_ant(payload):
    """
    双天线解调
    :param payload:
    :return:
    """
    signal_id = payload.get("signal_id", None)
    protocol = payload.get("protocol", None)

    os.chdir(matlab_path)
    eng = matlab.engine.start_matlab()
    try:
        logger.info("start matlab double_ant demode")
        eng.demod_double_ant(signal_id, protocol)
        eng.quit()
        os.chdir(celery_path)
        return True
    except Exception as exp:
        logger.error("double_ant demode error: %s" % str(exp))
        eng.quit()
        os.chdir(celery_path)
        return False


@shared_task()
def Demode_four_ant(payload):
    """
    双天线解调
    :param payload:
    :return:
    """
    signal_id = payload.get("signal_id", None)
    protocol = payload.get("protocol", None)

    os.chdir(matlab_path)
    eng = matlab.engine.start_matlab()
    try:
        logger.info("start matlab four_ant demode")
        eng.demod_four_ant(signal_id, protocol)
        eng.quit()
        os.chdir(celery_path)
        return True
    except Exception as exp:
        logger.error("four_ant demode error: %s" % str(exp))
        eng.quit()
        os.chdir(celery_path)
        return False
