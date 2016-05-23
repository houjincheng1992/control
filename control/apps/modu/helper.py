# coding=utf-8

from control.control import settings

from .models import DistriModel
from .models import PartableModel
from .models import TimetableModel
from .models import AisdataModel
from .models import SignalModel
from .tasks import *

from control.control.base import control_response
from control.control.base import randomname_maker
from control.control.err_msg import ModuErrorCode

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
    protocol = payload.get("protocol", None)
    distri_id = payload.get("distri_id", None)
    partable_id = payload.get("partable_id", None)
    timetable_id = make_id(action)
    sub_payload = {
        "action": action,
        "obtime": obtime,
        "height": height,
        "protocol": protocol,
        "distri_id": distri_id,
        "partable_id": partable_id,
        "timetable_id": timetable_id
    }
    timetable_model, error = TimetableModel.objects.create(distri_id=distri_id,
                                                           partable_id=partable_id,
                                                           timetable_id=timetable_id,
                                                           obtime=obtime,
                                                           protocol=protocol
                                                          )
    if not timetable_model:
        return control_response(code=ModuErrorCode.TIMETABLE_SAVED_FAILED, msg=error, ret_name_id="timetable_id")
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
    filename = payload.get("filename", None)
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
            filenameUpdate = filename
        else:
            filenameUpdate = filename + "_" + str(packageIndex)
        signal_id = make_id(action)
        sub_payload.update({"signal_id": signal_id})
        logger.info("sub_payload is %s" % sub_payload)
        signal_model, error = SignalModel.objects.create(filename=filenameUpdate,
                                                         partable_id=partable_id,
                                                         timetable_id=timetable_id,
                                                         aisdata_id=aisdata_id,
                                                         signal_id=signal_id,
                                                         snr=snr
                                                         )
        if not signal_model:
            return control_response(code=ModuErrorCode.SIGNAL_SAVED_FAILED, msg=error, ret_name_id="signal_id")
        matlab_create_aisSig.apply_async([sub_payload])
        signal_id_list.append(signal_id)
    return control_response(code=0,
                            msg="signal running",
                            ret_set=[signal_id_list],
                            ret_name_id="signal_id",
                            total_count=packagenum)
