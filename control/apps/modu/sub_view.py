# coding=utf-8

from control.control.err_msg import ModuErrorCode
from control.control.base import control_response

from .helper import create_ves_distri
from .helper import create_ves_parTalb
from .helper import create_time_table
from .helper import create_ves_data
from .helper import create_aissig
from .models import DistriModel
from .models import PartableModel
from .models import TimetableModel
from .models import  AisdataModel

from control.control.logger import getLogger

logger = getLogger(__name__)


def CreateDistri(payload):
    """
    :param payload:  创建信号所需数据
    :return:
    """
    # payload = self.payload
    # logger.info("payload is %s", payload)
    action = payload.get("action", None)
    filename = payload.get("filename", None)
    packagenum= payload.get("packagenum", None)
    lon = payload.get("lon", None)
    lat = payload.get("lat", None)
    height = payload.get("height", None)
    vesnum = payload.get("vesnum", None)
    distri_mode = payload.get("distri_mode", None)
    username = payload.get("owner")
    sub_payload = {
        "action": action,
        "filename": filename + '_' + action,
        "packagenum": packagenum,
        "lon": lon,
        "lat": lat,
        "height": height,
        "vesnum": vesnum,
        "distri_mode": distri_mode,
        "owner": username
    }
    ret_message = create_ves_distri(sub_payload)
    return ret_message


def CreatePartable(payload):
    """
    :payload: 创建信号所需数据
    :return:
    """
    action = payload.get("action", None)
    filename = payload.get("filename", None)
    packagenum = payload.get("packagenum", None)
    height = payload.get("height", None)
    vesnum = payload.get("vesnum", None)
    ant_pitch = payload.get("ant_pitch", None)
    ant_azimuth = payload.get("ant_azimuth", None)
    antenna_type = payload.get("ant_type", None)
    channel_type = payload.get("channel_type", None)
    distri_id = payload.get("distri_id", None)

    if distri_id is None:
        return control_response(code=ModuErrorCode.DISTRI_ID_MISSING, msg="distri_id is needed!")

    sub_payload = {
        "action": action,
        "filename": filename + '_' + action,
        "packagenum": packagenum,
        "height": height,
        "vesnum": vesnum,
        "ant_pitch": ant_pitch,
        "ant_azimuth": ant_azimuth,
        "antenna_type": antenna_type,
        "channel_type": channel_type,
        "distri_id": distri_id,
    }
    ret_message = create_ves_parTalb(sub_payload)
    return ret_message


def CreateTimetable(payload):
    """
    :return:
    """
    # payload = self.payload
    action = payload.get("action", None)
    filename = payload.get("filename", None)
    packagenum = payload.get("filename", None)
    obtime = payload.get("obtime", None)
    height = payload.get("height", None)
    protocol = payload.get("protocol", None)
    distri_id = payload.get("distri_id", None)
    partable_id = payload.get("partable_id", None)
    if partable_id is None:
        return control_response(code=ModuErrorCode.PARTABLE_ID_MISSING, msg="partable_id is needed!")
    if distri_id is None:
        distri_id = DistriModel.get_distriid_by_id(partable_id)

    sub_payload = {
        "action": action ,
        "filename": filename + '_' + action,
        "packagenum": packagenum,
        "obtime": obtime,
        "height": height,
        "protocol": protocol,
        "distri_id": distri_id,
        "partable_id": partable_id,
    }
    ret_message = create_time_table(sub_payload)
    return ret_message


def CreateAisdata(payload):
    """
    :param payload: 创建所需信号
    :return:
    """
    # payload = self.payload
    action = payload.get("action", None)
    filename = payload.get("filename", None)
    packagenum = payload.get("packagenum", None)
    distri_id = payload.get("distri_id", None)
    timetable_id = payload.get("timetable_id", None)

    if timetable_id is None:
        return control_response(code=ModuErrorCode.TIMETABLE_ID_MISSING, msg="timetable_id is needed!")
    if distri_id is None:
        partable_id = PartableModel.get_partableid_by_id(timetable_id)
        distri_id = DistriModel.get_distriid_by_id(partable_id)
    sub_payload = {
        "action": action,
        "filename": filename + '_' + action,
        "packagenum": packagenum,
        "distri_id": distri_id,
        "timetable_id": timetable_id,
    }
    ret_message = create_ves_data(sub_payload)
    return ret_message


def CreateSignal(payload):
    """
    产生AIS信号
    :param payload: 包含必要的关于产生timetable的参数
    :return: aisSig_Path 存储AISSig的路径
    """
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
    if aisdata_id is None:
        return control_response(code=ModuErrorCode.AISDATA_ID_MISSING, msg="aisdata_id is needed!")
    if timetable_id is None:
        timetable_id = TimetableModel.get_timetableid_by_id(aisdata_id)
    if partable_id is None:
        partable_id = PartableModel.get_partableid_by_id(timetable_id)
    sub_payload = {
        "action": action,
        "filename": filename + '_' + action,
        "packagenum": packagenum,
        "obtime": obtime,
        "vesnum": vesnum,
        "height": height,
        "partable_id": partable_id,
        "timetable_id": timetable_id,
        "aisdata_id": aisdata_id,
        "snr": snr
    }
    ret_message = create_aissig(sub_payload)
    return ret_message


class Router():
    """
    chose fuction following different action
    """
    ACTION_LIST = ["distri", "partable", "timetable", "aisdata", "signal"]
    FUNCTION_LIST = [CreateDistri, CreatePartable, CreateTimetable, CreateAisdata, CreateSignal]
    # 获取ACTION对应关系
    ACTION = {}
    for actionIndex in range(len(ACTION_LIST)):
        ACTION.update({ACTION_LIST[actionIndex]: FUNCTION_LIST[actionIndex]})

    def __init__(self, payload):
        self.payload = payload

    def Actionrouter(self):
        """
        :param payload: 获取action
        :return:
        """
        payload = self.payload
        action = payload.get("action", None)
        if action is not None:
            logger.info("Current action is: %s" % action)
            ret_message = self.ACTION[action](payload)
            return ret_message

        action_all = payload.get("action_all", None)
        if action_all is True:
            ret = {}
            for action in self.ACTION_LIST:
                payload.update({"action": action})
                if action is not None:
                    logger.info("Current action is: %s" % action)
                    ret_message = self.ACTION[action](payload)
                    payload.update({ret_message["ret_name_id"]: ret_message["ret_set"][0]})
                    ret.update(ret_message)
            return ret
        return control_response(code=ModuErrorCode.ACTION_GET_FAILED, msg="action 获取失败")

