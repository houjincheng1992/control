# coding=utf-8

import os
import matlab.engine

from celery import shared_task

from control.control.base import get_path
from control.control.logger import getLogger

logger = getLogger(__name__)

"""
创建matlab引擎， 调用matlab函数
"""


matlab_path = get_path.MATLAB_FILE_PATH
celery_path = get_path.CELERY_PATH


@shared_task
def matlab_create_ves_distri(payload):
    """
    调用matlab产生船舶分布矩阵
    :param payload:包含需要产生船舶分布信息的参数
    :return: distri_id 船舶分布矩阵的id
    :uid_sid: 用户ID以及信号ID
    """
    action = payload.get("action", None)
    lon = payload.get("lon", None)
    lat = payload.get("lat", None)
    height = payload.get("height", None)
    vesNum = payload.get("vesNum", None)
    distri_mode = payload.get("distri_mode", None)
    distri_id = payload.get("distri_id", None)
    os.chdir(matlab_path)
    logger.info(os.getcwd())
    eng = matlab.engine.start_matlab()
    try:
        logger.info("start matlab_distri")
        eng.F_genDistri(lon, lat, height, vesNum, distri_mode, distri_id)
        eng.quit()
        os.chdir(celery_path)
        return True
    except Exception as exp:
        logger.error("distri running error: %s" % str(exp))
        eng.quit()
        os.chdir(celery_path)
        return False


@shared_task
def matlab_create_ves_parTable(payload):
    """
    调用matlab产生parTable
    :param payload:包含需要产生船舶分布信息的参数
    :return: parTable_id 存储parTable的id
    :uid 用户ID
    """
    action = payload.get("action", None)
    height = payload.get("height", None)
    ant_pitch = payload.get("ant_pitch", None)
    ant_azimuth = payload.get("ant_azimuth", None)
    antenna_type = payload.get("antenna_type", None)
    channel_type = payload.get("channel_type")
    distri_id = payload.get("distri_id", None)
    partable_id = payload.get("partable_id", None)
    os.chdir(matlab_path)
    eng = matlab.engine.start_matlab()
    try:
        logger.info("start matlab_partable")
        eng.F_genParTable(height, ant_pitch, ant_azimuth, antenna_type, channel_type, distri_id, partable_id)
        eng.quit()
        os.chdir(celery_path)
        return True
    except Exception as exp:
        logger.error("partable running error: %s" % str(exp))
        eng.quit()
        os.chdir(celery_path)
        return False


@shared_task
def matlab_create_time_table(payload):
    """
    调用matlab产生parTable
    :param payload:包含需要产生船舶分布信息的参数
    :return: parTable_id 存储parTable的id
    """
    action = payload.get("action", None)
    obtime = payload.get("obtime", None)
    protocol = payload.get("protocol", None)
    height = payload.get("height", None)
    distri_id = payload.get("distri_id", None)
    partable_id = payload.get("partable_id", None)
    timetable_id = payload.get("timetable_id", None)
    os.chdir(matlab_path)
    eng = matlab.engine.start_matlab()
    try:
        logger.info("start matlab_timetable")
        eng.F_genTimeTable(obtime, protocol, height, distri_id, partable_id, timetable_id)
        eng.quit()
        os.chdir(celery_path)
        return True
    except Exception as exp:
        logger.error("timetable running error: %s" % str(exp))
        eng.quit()
        os.chdir(celery_path)
        return False


@shared_task
def matlab_create_ves_data(payload):
    """
    调用matlab产生AISData
    :param payload:包含需要产生船舶分布信息的参数
    :return: send_data_id 存储AISData的id
    :uid_sid: 用户ID以及信号ID
    """
    action = payload.get("action", None)
    distri_id = payload.get("distri_id", None)
    timetable_id = payload.get("timetable_id", None)
    aisdata_id = payload.get("aisdata_id", None)
    os.chdir(matlab_path)
    eng = matlab.engine.start_matlab() # 启动matlab程序
    try:
        logger.info("start matlab_aisdata")
        eng.F_genAISData(distri_id, timetable_id, aisdata_id)
        eng.quit()
        os.chdir(celery_path)
        return True
    except Exception as exp:
        logger.error("aisdata running error: %s" % str(exp))
        eng.quit()
        os.chdir(celery_path)
        return False


@shared_task
def matlab_create_aisSig(payload):
    """
    调用matlab产生Singal
    :param payload:包含需要产生船舶分布信息的参数
    :return: aisSig_id 存储AIS_Signal的id
    """
    action = payload.get("action", None)
    obtime = payload.get("obtime", None)
    vesnum = payload.get("vesnum", None)
    height = payload.get("height", None)
    snr = payload.get("snr", None)
    partable_id = payload.get("partable_id", None)
    timetable_id = payload.get("timetable_id", None)
    aisdata_id = payload.get("aisdata_id", None)
    signal_id = payload.get("signal_id", None)
    os.chdir(matlab_path)
    logger.info("The current path is %s" % matlab_path)
    eng = matlab.engine.start_matlab()
    try:
        logger.info("start matlab_signal")
        eng.F_genAISSig(obtime, vesnum, height, snr, partable_id, timetable_id, aisdata_id, signal_id)
        eng.quit()
        os.chdir(celery_path)
        return True
    except Exception as exp:
        logger.error("signal running error: %s" % str(exp))
        eng.quit()
        os.chdir(celery_path)
        return False
