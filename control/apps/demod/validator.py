# coding=utf-8

from django.utils.translation import ugettext as _
from rest_framework import serializers

from control.apps.modu.models import SignalModel



ANT_TYPE = {
    "single_ant": True,
    "double_ant": True,
    "four_ant": True
}

PROTOCOL_TYPE = {
    "SOTDMA": True
}

SYNC_TYPE = {
    "DEFAULT": True
}


def signal_id_validator(signal_id):
    """
    validate signal_id
    :param signal_id:
    :return:
    """
    if isinstance(signal_id, list):
        for key_signal_id in signal_id:
            if not SignalModel.signal_exist_by_id(key_signal_id):
                raise serializers.ValidationError(u"%s is not exist in SignalModel!" % key_signal_id)
    if not SignalModel.signal_exist_by_id(signal_id):
        raise serializers.ValidationError(u"%s is not exist in SignalModel!" % signal_id)

def ant_type_validator(ant_type):
    if isinstance(ant_type, list):
        for key_ant_type in ant_type:
            if key_ant_type not in ANT_TYPE:
                raise serializers.ValidationError(u"ant_type is invalid！")
    if ant_type not in ANT_TYPE:
        raise serializers.ValidationError(u"ant_type is invalid!")

def protocol_validator(protocol_type):
    """
    validator protocol
    :return:
    """
    if isinstance(protocol_type, list):
        for key_protocol_type in protocol_type:
            if key_protocol_type not in PROTOCOL_TYPE:
                raise serializers.ValidationError(u"protocol_type is invalid!")
    if protocol_type not in PROTOCOL_TYPE:
        raise serializers.ValidationError(u"protocol_type is invalid")

def sync_type_validator(sync_type):
    """
    validate sync_type
    :param sync_type:
    :return:
    """
    if isinstance(sync_type, list):
        for key_sync_type in sync_type:
            if key_sync_type not in SYNC_TYPE:
                raise serializers.ValidationError(u"sync_type is invalid!")
    if sync_type not in SYNC_TYPE:
        raise serializers.ValidationError(u"sync_type is invalid!")