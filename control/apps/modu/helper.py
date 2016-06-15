# coding=utf-8
from __future__ import division

from os.path import getsize
from os.path import join

from django.conf import settings

from control.control import settings
from control.control.base import control_response
from control.control.base import randomname_maker
from control.control.err_msg import ModuErrorCode
from control.control.err_msg import DESCRIBErrorCode

from .models import AisdataModel
from .models import DistriModel
from .models import PartableModel
from .models import SignalModel
from .models import TimetableModel


from .models import ScheduleModel
from .tasks import *

from control.control.logger import getLogger
logger = getLogger(__name__)

def make_id(action):
    while True:
        distri_id = "%s-%s" % (settings.DISTRI_PREFIX, randomname_maker())
        partable_id = "%s-%s" % (settings.PARTABLE_PREFIX, randomname_maker())
        timetable_id = "%s-%s" % (settings.TIMETABLE_PREFIX, randomname_maker())
        aisdata_id = "%s-%s" % (settings.AISDATA_PREFIX, randomname_maker())
        signal_id = "%s-%s" % (settings.SIGNAL_PREFIX, randomname_maker())
        if action == "distri":
            if not DistriModel.distri_exist_by_id(distri_id):
                return distri_id
        if action == "partable":
            if not PartableModel.partable_exist_by_id(partable_id):
                return partable_id
        if action == "timetable":
            if not TimetableModel.timetable_exist_by_id(timetable_id):
                return timetable_id
        if action == "aisdata":
            if not AisdataModel.aisdata_exist_by_id(aisdata_id):
                return aisdata_id
        if action == "signal":
            if not SignalModel.signal_exist_by_id(signal_id):
                return signal_id


def create_ves_distri(payload):
    """
    产生船舶分布矩阵
    :param payload:包含需要产生船舶分布信息的参数
    :return:
    """
    action = payload.get("action", None)
    lon = payload.get("lon", None)
    lat = payload.get("lat", None)
    height = payload.get("height", None)
    vesNum = payload.get("vesnum", None)
    distri_mode = payload.get("distri_mode", None)
    username = payload.get("owner", None)
    distri_id = make_id(action)


    sub_payload = {
        "action": action,
        "lon": lon,
        "lat": lat,
        "height": height,
        "vesNum": vesNum,
        "distri_mode": distri_mode,
        "distri_id": distri_id,
        "owner": username
    }
    distri_model, error = DistriModel.objects.create(user=username,
                                                     distri_id=distri_id,
                                                     distri_lon=lon,
                                                     distri_lat=lat,
                                                     distri_height=height,
                                                     distri_ves_num=vesNum,
                                                     distri_mode=distri_mode
                                                     )
    if not distri_model:
        return control_response(code=ModuErrorCode.DISTRI_SAVED_FAILED, msg=error, ret_name_id="distri_id")
    if settings.IF_RUN_MATLAB == 'True':
        matlab_create_ves_distri.apply_async([sub_payload])
    return control_response(code=0, msg="distri running", ret_set=[distri_id], ret_name_id="distri_id")

def create_ves_parTalb(payload):
    """
    产生船舶功率频偏时延DOA参数
    :param payload:包含需要产生船舶分布信息的参数
    :return: parTable_id 船舶参数矩阵的id
    """
    action = payload.get("action", None)
    height = payload.get("height", None)
    vesnum = payload.get("vesnum", None)
    ant_pitch = payload.get("ant_pitch", None)
    ant_azimuth = payload.get("ant_azimuth", None)
    antenna_type = payload.get("antenna_type", None)
    channel_type = payload.get("channel_type", None)
    distri_id = payload.get("distri_id", None)
    partable_id = make_id(action)
    sub_payload = {
        "action": action,
        "height": height,
        "vesnum": vesnum,
        "ant_pitch": ant_pitch,
        "ant_azimuth": ant_azimuth,
        "antenna_type": antenna_type,
        "channel_type": channel_type,
        "distri_id": distri_id,
        "partable_id": partable_id
    }
    parTable_model, error = PartableModel.objects.create(distri_id=distri_id,
                                                         partable_id=partable_id,
                                                         pitch=ant_pitch,
                                                         azimuth=ant_azimuth,
                                                         antenna_type=antenna_type,
                                                         channel_type=channel_type
                                                         )
    if not parTable_model:
        return control_response(code=ModuErrorCode.PARTABLE_SAVED_FAILED, msg=error, ret_name_id="partable_id")
    if settings.IF_RUN_MATLAB == 'True':
        matlab_create_ves_parTable.apply_async([sub_payload])
    return control_response(code=0, msg="parTable running", ret_set=[partable_id], ret_name_id="partable_id")


def create_time_table(payload):
    """
    产生timetable
    :param: payload 包含必要的关于产生timetable的参数
    :return: timeTable_id 存储timeTable的id
    """
    action = payload.get("action", None)
    obtime = payload.get("obtime", None)
    height = payload.get("height", None)
    transInterval = payload.get("transInterval", None)
    protocol = payload.get("protocol", None)
    distri_id = payload.get("distri_id", None)
    partable_id = payload.get("partable_id", None)
    timetable_id = make_id(action)
    sub_payload = {
        "action": action,
        "obtime": obtime,
        "height": height,
        "transInterval": transInterval,
        "protocol": protocol,
        "distri_id": distri_id,
        "partable_id": partable_id,
        "timetable_id": timetable_id
    }
    logger.info("payload is %s" % sub_payload)
    timetable_model, error = TimetableModel.objects.create(distri_id=distri_id,
                                                           partable_id=partable_id,
                                                           timetable_id=timetable_id,
                                                           obtime=obtime,
                                                           transinterval=transInterval,
                                                           protocol=protocol
                                                          )
    if not timetable_model:
        return control_response(code=ModuErrorCode.TIMETABLE_SAVED_FAILED, msg=error, ret_name_id="timetable_id")
    if settings.IF_RUN_MATLAB == 'True':
        matlab_create_time_table.apply_async([sub_payload])
    return control_response(code=0, msg="timetable running", ret_set=[timetable_id], ret_name_id="timetable_id")

def create_ves_data(payload):
    """
    产生船舶发送数据
    :param: payload 包含必要的输入信息
    :return: send_data_id 发送信息表的id
    """
    action = payload.get("action", None)
    distri_id = payload.get("distri_id", None)
    timetable_id = payload.get("timetable_id", None)
    aisdata_id = make_id(action)

    sub_payload = {
        "action": action,
        "distri_id": distri_id,
        "timetable_id": timetable_id,
        "aisdata_id": aisdata_id
    }
    aisdata_model, error = AisdataModel.objects.create(distri_id=distri_id,
                                                       timetable_id=timetable_id,
                                                       aisdata_id=aisdata_id
                                                       )
    if not aisdata_model:
        return control_response(code=ModuErrorCode.AISDATA_SAVED_FAILED, msg=error, ret_name_id="aisdata_id")
    if settings.IF_RUN_MATLAB == 'True':
        matlab_create_ves_data.apply_async([sub_payload])
    return control_response(code=0, msg="aisdate running", ret_set=[aisdata_id], ret_name_id="aisdata_id")

def create_aissig(payload):
    """
    产生AIS信号
    :param payload: 包含必要的关于产生timetable的参数
    :return: aisSig_Path 存储AISSig的路径
    """
    # action = payload("action", None)
    action = payload.get("action", None)
    name_signal = payload.get("name_signal", None)
    packagenum = payload.get("packagenum", None)
    obtime = payload.get("obtime", None)
    vesnum = payload.get("vesnum", None)
    height = payload.get("height", None)
    partable_id = payload.get("partable_id", None)
    timetable_id = payload.get("timetable_id", None)
    aisdata_id = payload.get("aisdata_id", None)
    snr = payload.get("snr")
    sub_payload = {
        "action": action,
        "obtime": obtime,
        "vesnum": vesnum,
        "height": height,
        "partable_id": partable_id,
        "timetable_id": timetable_id,
        "aisdata_id": aisdata_id,
        # "signal_id": signal_id,
        "snr": snr
    }
    signal_id_list = []
    for packageIndex in range(packagenum):
        if packagenum == 1:
            name_signal_update = name_signal
        else:
            name_signal_update = name_signal + "_" + str(packageIndex)
        signal_id = make_id(action)
        sub_payload.update({"signal_id": signal_id})
        signal_model, error = SignalModel.objects.create(name_signal=name_signal_update,
                                                         timetable_id=timetable_id,
                                                         partable_id=partable_id,
                                                         aisdata_id=aisdata_id,
                                                         signal_id=signal_id,
                                                         snr=snr
                                                         )
        if not signal_model:
            return control_response(code=ModuErrorCode.SIGNAL_SAVED_FAILED, msg=error, ret_name_id="signal_id")
        if settings.IF_RUN_MATLAB == 'True':
            matlab_create_aisSig.apply_async([sub_payload])
        signal_id_list.append(signal_id)
    return control_response(code=0,
                            msg="signal running",
                            ret_set=[signal_id_list],
                            ret_name_id="signal_id",
                            total_count=packagenum)


def Getdescribe(payload):
    """
    获取文件信息
    :param payload:
    :return:
    """
    signal_id = payload.get("signal_id")
    try:
        createtime = get_createtime(signal_id)
        signalsize = get_save_signalsize(signal_id)
        logger.info("siganlsize is %d" % signalsize)
        schedule = get_save_schedule(signal_id)
        return control_response(code=0,
                                msg="describe success!",
                                ret_set={"createtime": createtime, "signalsize": signalsize, "schedule": schedule}
                                )
    except Exception as exp:
        logger.error("describe error: %s" % str(exp))
        return control_response(code=DESCRIBErrorCode.GET_DESCRIBE_FAILED, msg="describe failed!")


def Getcreatetime(payload):
    """
    获取文件创建时间
    :param payload:
    :return:
    """
    signal_id = payload.get("signal_id")
    try:
        createtime = get_createtime(signal_id)
        return control_response(code=0, msg="describe success!", ret_set={"createtime": createtime})
    except Exception as exp:
        logger.error("get createtime error: %s" % str(exp))
        return control_response(code=DESCRIBErrorCode.GET_CREATETIME_FAILED, msg=str(exp))

def Getsignalsize(payload):
    """
    获取文件大小
    :param payload:
    :return:
    """
    signal_id = payload.get("signal_id")
    try:
        signalsize = get_save_signalsize(signal_id)
        return control_response(code=0, msg="get signal size success!", ret_set={"signalsize": signalsize})
    except Exception as exp:
        control_response(code=DESCRIBErrorCode.GET_SIGNALSIZE_FAILED, msg=str(exp))


def Getschedule(payload):
    """
    获取运行进度
    :param payload:
    :return:
    """
    signal_id = payload.get("signal_id")
    try:
        schedule = get_save_schedule(signal_id)
        logger.info("schedule is %d" % schedule)
        return control_response(code=0, msg="get schedule success!", ret_set=[{"schedule": schedule}])
    except Exception as exp:
        return control_response(code=DESCRIBErrorCode.GET_SCHEDULE_FAILED, msg=str(exp))


def Getdetail(payload):
    """
    获取信号的详细参数信息
    :param payload:
    :return:
    """
    try:
        signal_id = payload.get("signal_id")
        detail_info = get_signal_detail(signal_id)
        return control_response(code=0, ret_set=detail_info)
    except Exception as exp:
        logger.info("get signal detail info error:%s" % str(exp))
        return control_response(code=DESCRIBErrorCode.GET_DETAIL_FAILED, msg=str(exp))


# def Deletesignal(payload):
#     """
#     删除信号信息
#     :param payload:
#     :return:
#     """
#     signal_id = payload.get("signal_id")
#     if isinstance(signal_id, list):
#         for


def get_createtime(signal_id):
    """
    获取创建时间
    :param signal_id:
    :return:
    """
    signal = SignalModel.get_signal_by_id(signal_id)
    return signal.create_datetime


def get_save_signalsize(signal_id):
    """
    获取信号大小并保存在数据表中
    :param signal_id:
    :return:
    """
    signalpath = os.path.join(get_path.MATLAB_FILE_PATH, "DATA/aisSig", signal_id)
    signalsize = getdirsize(signalpath)
    logger.info("signal size is %d" % signalsize)
    status_model, error = SignalModel.status_size_save(signal_id=signal_id, signalsize=signalsize)
    logger.info("status_model is %s" % status_model)
    if not status_model:
        return control_response(code=DESCRIBErrorCode.SAVE_STATUS_ERROR, msg=error)
    return signalsize


def get_save_schedule(signal_id):
    """
    计算信号运行进度
    :param signal_id:
    :return:
    """
    try:
        timetable = SignalModel.get_signal_by_id(signal_id).timetable
        obtime = timetable.obtime
        transinterval = timetable.transinterval
        total_filenum = obtime / transinterval + 1
        rate_matlab, filenum = get_matlab_rate(total_filenum=total_filenum, signal_id=signal_id)
        if filenum == total_filenum:
            rate = filenum / total_filenum
        else:
            rate = rate_matlab
        rate = round(rate, 2)
        status_model, error = SignalModel.status_schedule_save(signal_id=signal_id, schedule=rate)
        if not status_model:
            return control_response(code=DESCRIBErrorCode.SAVE_STATUS_ERROR, msg=error)
        return rate
    except Exception as exp:
        logger.error("get schedule error: %s" % str(exp))
        return 0


def get_signal_detail(signal_id):
    """
    获取信号详细参数信息
    :param signal_id:
    :return:
    """
    if isinstance(signal_id, list):
        detail_info = []
        for key_signal_id in signal_id:
            info = get_par_by_signal_id(key_signal_id)
            detail_info.append(info)
        return detail_info
    else:
        detail_info = get_par_by_signal_id(signal_id)
        return detail_info


def getdirsize(dir):
    """
    计算信号大小
    :param dir: 需要计算文件夹的完整路径
    :return: 文件夹下所有文件的大小， 以Kb为单位
    """
    logger.info("the current dir is %s" % dir)
    size = 0L
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return round(size/1024)


def getfilenum(signal_id):
    """
    获取当前信号已产生文件数
    :param signal_id:
    :return:
    """
    signalpath = os.path.join(get_path.MATLAB_FILE_PATH, "DATA/aisSig", signal_id)
    filenum = 0
    for root, dirs, files in os.walk(signalpath):
        filelength = len(files)
        logger.info(filelength)
        if filelength != 0:
            filenum = filenum + filelength
    return filenum


def get_matlab_rate(total_filenum, signal_id):
    """
    获取matlab 进度
    :return:
    """
    # 获取model_id
    aisdata_id = SignalModel.get_aisdata_id_by_siganl_id(signal_id)
    timetable_id = SignalModel.get_timetable_id_by_signal_id(signal_id)
    partable_id = SignalModel.get_partable_id_by_signal_id(signal_id)
    distri_id = PartableModel.get_distri_id_by_partable_id(partable_id)
    #获取model_rate
    distri_rate = ScheduleModel.get_schedule_by_model_id(model_id=distri_id)
    partable_rate = ScheduleModel.get_schedule_by_model_id(model_id=partable_id)
    timetable_rate = ScheduleModel.get_schedule_by_model_id(model_id=timetable_id)
    aisdata_rate = ScheduleModel.get_schedule_by_model_id(model_id=aisdata_id)
    signal_rate = ScheduleModel.get_schedule_by_model_id(model_id=signal_id)

    filenum = getfilenum(signal_id)
    signal_all_rate = (signal_rate + filenum)/total_filenum
    rate = distri_rate * 0.05 + partable_rate * 0.05 + timetable_rate * 0.35 + aisdata_rate * 0.05 + signal_all_rate * 0.5
    return rate, filenum


def get_par_by_signal_id(signal_id):
    try:
        # 获取各个表
        signal = SignalModel.get_signal_by_id(signal_id)
        aisdata_id = SignalModel.get_aisdata_id_by_siganl_id(signal_id)
        aisdata = AisdataModel.get_aisdata_by_id(aisdata_id)
        timetable_id = SignalModel.get_timetable_id_by_signal_id(signal_id)
        timetable = TimetableModel.get_timetable_by_id(timetable_id)
        partable_id = SignalModel.get_partable_id_by_signal_id(signal_id)
        partable = PartableModel.get_partbale_by_id(partable_id)
        distri_id = PartableModel.get_distri_id_by_partable_id(partable_id)
        distri = DistriModel.get_distri_by_id(distri_id)
        # 获取个表中对应信号的参数信息
        par = {
            "lat": distri.distri_lat,
            "lon": distri.distri_lon,
            "height": distri.distri_height,
            "vesnum": distri.distri_ves_num,
            "distri_mode": distri.distri_mode,
            "pitch": partable.pitch,
            "azimuth": partable.azimuth,
            "ant_type": partable.antenna_type,
            "channel_type": partable.channel_type,
            "obtime": timetable.obtime,
            "transinterval": timetable.transinterval,
            "protocol": timetable.protocol,
            "name_sinal": signal.name_signal,
            "snr": signal.snr
            }
        return par
    except Exception as exp:
        logger.error("get parameter from database error: %s" % str(exp))
        return False