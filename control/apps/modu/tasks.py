# coding=utf-8

import os
import matlab.engine

from datetime import time
from os.path import getsize
from os.path import join

from celery import shared_task

from control.control import settings
from control.control.base import get_path
from control.control.base import control_response

from .models import PartableModel
from .models import SignalModel
from .models import ScheduleModel

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
        logger.info("the current path is %s" % os.getcwd())
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
    transInterval = payload.get("transInterval", None)
    distri_id = payload.get("distri_id", None)
    partable_id = payload.get("partable_id", None)
    timetable_id = payload.get("timetable_id", None)
    os.chdir(matlab_path)
    eng = matlab.engine.start_matlab()
    try:
        logger.info("start matlab_timetable")
        logger.info("payload is %s", payload)
        eng.F_genTimeTable(obtime, protocol, height, transInterval, distri_id, partable_id, timetable_id)
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
        logger.info("payload is %s" % payload)
        eng.F_genAISSig(obtime, vesnum, height, snr, partable_id, timetable_id, aisdata_id, signal_id)
        eng.quit()
        os.chdir(celery_path)
        return True
    except Exception as exp:
        logger.error("signal running error: %s" % str(exp))
        eng.quit()
        os.chdir(celery_path)
        return False


# def signal_info_save(signal_id_list):
#     """
#     保存信号的状态信息
#     :param signal_id: 信号id
#     :return: None
#     """
#     signalId = signal_id_list[0][0]
#     seconds = settings.SAVE_PERIED  # 获取保存周期
#     try:
#         if isinstance(signalId, list):
#             for signal_id in signalId:
#                 time.sleep(seconds)
#                 get_save_schedule(signal_id=signal_id)
#                 get_save_signalsize(signal_id)
#             return True
#         time.sleep(seconds)
#         get_save_schedule(signal_id=signalId)
#         get_save_signalsize(signalId)
#         return True
#     except Exception as exp:
#         logger.error("%s info save error: %s" % (signalId, exp))
#         return False
#
#
# def get_createtime(signal_id):
#     """
#     获取创建时间
#     :param signal_id:
#     :return:
#     """
#     try:
#         signal = SignalModel.get_signal_by_id(signal_id)
#         return signal.create_datetime
#     except Exception as exp:
#         return False
#
#
# def get_save_signalsize(signal_id):
#     """
#     获取信号大小并保存在数据表中
#     :param signal_id:
#     :return:
#     """
#     signalpath = os.path.join(get_path.MATLAB_FILE_PATH, "DATA/aisSig", signal_id)
#     signalsize = getdirsize(signalpath)
#     try:
#         SignalModel.status_size_save(signal_id=signal_id, signalsize=signalsize)
#         return signalsize
#     except Exception as exp:
#         return False
#
#
# def get_save_schedule(signal_id):
#     """
#     计算信号运行进度
#     :param signal_id:
#     :return:
#     """
#     try:
#         timetable = SignalModel.get_signal_by_id(signal_id).timetable
#         obtime = timetable.obtime
#         transinterval = timetable.transinterval
#         total_filenum = obtime / transinterval + 1
#         rate_matlab, filenum = get_matlab_rate(total_filenum=total_filenum, signal_id=signal_id)
#         if filenum == total_filenum:
#             rate = filenum / total_filenum
#         else:
#             rate = rate_matlab
#         SignalModel.status_schedule_save(signal_id=signal_id, schedule=rate)
#         return rate
#     except Exception as exp:
#         return 0
#
#
# def getdirsize(dir):
#     """
#     计算信号大小
#     :param dir: 需要计算文件夹的完整路径
#     :return: 文件夹下所有文件的大小， 以Kb为单位
#     """
#     logger.info("the current dir is %s" % dir)
#     size = 0L
#     for root, dirs, files in os.walk(dir):
#         size += sum([getsize(join(root, name)) for name in files])
#     return size/1024
#
#
# def get_matlab_rate(total_filenum, signal_id):
#     """
#     获取matlab 进度
#     :return:
#     """
#     # 获取model_id
#     aisdata_id = SignalModel.get_aisdata_id_by_siganl_id(signal_id)
#     timetable_id = SignalModel.get_timetable_id_by_signal_id(signal_id)
#     partable_id = SignalModel.get_partable_id_by_signal_id(signal_id)
#     distri_id = PartableModel.get_distri_id_by_partable_id(partable_id)
#     #获取model_rate
#     distri_rate = ScheduleModel.get_schedule_by_model_id(model_id=distri_id)
#     partable_rate = ScheduleModel.get_schedule_by_model_id(model_id=partable_id)
#     timetable_rate = ScheduleModel.get_schedule_by_model_id(model_id=timetable_id)
#     aisdata_rate = ScheduleModel.get_schedule_by_model_id(model_id=aisdata_id)
#     signal_rate = ScheduleModel.get_schedule_by_model_id(model_id=signal_id)
#
#     filenum = getfilenum(signal_id)
#     signal_all_rate = (signal_rate + filenum)/total_filenum
#     rate = distri_rate * 0.05 + partable_rate * 0.05 + timetable_rate * 0.35 + aisdata_rate * 0.05 + signal_all_rate * 0.5
#     return rate, filenum
#
#
# def getfilenum(signal_id):
#     """
#     获取当前信号已产生文件数
#     :param signal_id:
#     :return:
#     """
#     signalpath = os.path.join(get_path.MATLAB_FILE_PATH, "DATA/aisSig", signal_id)
#     filenum = 0
#     for root, dirs, files in os.walk(signalpath):
#         filelength = len(files)
#         logger.info(filelength)
#         if filelength != 0:
#             filenum = filenum + filelength
#     return filenum
