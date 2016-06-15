# coding=utf-8

from .validator import *

from control.control.logger import getLogger
logger = getLogger(__name__)


class CheckProbSerializer(serializers.Serializer):
    """
    解调序列化函数
    """
    action = serializers.CharField(
        max_length=20,
        required=False,
        validators=[action_validator]
    )

    demodSignal_id = serializers.CharField(
        max_length=20,
        required=True,
        validators=[demodSignal_id_validator]
    )
