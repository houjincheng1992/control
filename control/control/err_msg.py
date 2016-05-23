# coding=utf-8
from django.utils.translation import ugettext as _
from control.control.logger import getLogger

logger = getLogger(__name__)

PARAMETER_CODE = {
    # distri
    "distri_id": 10001,
    "distri_lon": 10002,
    "distri_lat": 10003,
    "distri_height": 10004,
    "distri_ves_num": 10005,
    "distri_mode": 10006
}

PARAMETER_MSG = {
    10001: _(u"参数distri_id不合法"),
    10002: _(u"参数distri_lon不合法"),
    10003: _(u"参数distri_lat不合法"),
    10004: _(u"参数distri_height不合法"),
    10005: _(u"参数distri_ves_num不合法"),
    10006: _(u"参数distri_mode不合法")
}

class ModuErrorCode(object):
    ACTION_GET_FAILED = 20000

    DISTRI_SAVED_FAILED = 20001
    DISTRI_RUNNING_FAILED = 20002
    DISTRI_ID_MISSING = 20003

    PARTABLE_SAVED_FAILED = 20011
    PARTABLE_RUNNING_FAILED = 20012
    PARTABLE_ID_MISSING = 20013

    TIMETABLE_SAVED_FAILED = 20021
    TIMETABLE_RUNNING_FAILED = 20022
    TIMETABLE_ID_MISSING = 20023

    AISDATA_SAVED_FAILED = 20031
    AISDATA_RUNNING_FAILED = 20032
    AISDATA_ID_MISSING = 20033

    SIGNAL_SAVED_FAILED = 20041
    SIGNAL_RUNNING_FAILED = 20042
    SIGNAL_ID_MISSING = 20043

ACTIN_MSG = {
    20000: _(u"action 丢失")
}

DISTRI_MSG = {
    20001: _(u"保存Distri数据异常"),
    20002: _(u"Distri数据运行异常"),
    20003: _(u"distri_id is missing")
}

PARTABLE_MSG = {
    20011: _(u"保存Partable数据异常"),
    20012: _(u"Partable数据运行异常"),
    20013: _(u"partable_id is missing")
}

TIMETABLE_MSG = {
    20021: _(u"保存Timetable数据异常"),
    20022: _(u"Timetable数据运行异常"),
    20023: _(u"timetable_id is missing")
}

AISDATA_MSG = {
    20031: _(u"保存Aisdata数据异常"),
    20032: _(u"Aisdata数据运行异常"),
    20033: _(u"aisdata_id is missing")
}

SIGNAL_MSG = {
    20041: _(u"保存Singnal数据异常"),
    20042: _(u"Signal数据运行异常"),
    20043: _(u"signal_id is missing")
}

class DEMODErrorCode():
    ANT_TYPE_INVALID = 30000
    