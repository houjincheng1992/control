# coding=utf-8

from django.utils.translation import ugettext as _
from rest_framework import serializers

from control.apps.demod.models import DemodModel

ACTION = {
    "untheory": True,
    "theory": True
}


def action_validator(action):
    """
    validate action
    :param action:
    :return:
    """
    if isinstance(action, list):
        for key_action in action:
            if key_action not in ACTION:
                raise serializers.ValidationError(u"action is invalid!")
    if action not in ACTION:
        raise serializers.ValidationError(u"action is invalid!")

def demodSignal_id_validator(demodSignal_id):
    """
    validate demodSignal_id
    :param demodSignal_id:
    :return:
    """
    if isinstance(demodSignal_id, list):
        for key_demodSignal_id in demodSignal_id:
            if DemodModel.demod_exist_by_id(key_demodSignal_id):
                raise serializers.ValidationError(u"demodSignal_id is not exist in DemodModel!")
    if DemodModel.demod_exist_by_id(demodSignal_id):
        raise serializers.ValidationError(u"demodSignal_id is not exist in DemodModel!")


