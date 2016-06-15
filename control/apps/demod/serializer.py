# coding=utf-8

from .validator import *

from control.control.logger import getLogger
logger = getLogger(__name__)


class DemodSignalSerializer(serializers.Serializer):
    """
    解调序列化函数
    """
    signal_id = serializers.CharField(
        max_length=20,
        required=True,
        validators=[signal_id_validator]
    )

    ant_type = serializers.CharField(
        max_length=20,
        required=False,
        validators=[ant_type_validator]
    )

    protocol = serializers.CharField(
        max_length=20,
        required=False,
        validators=[protocol_validator]
    )

    sync_type = serializers.CharField(
        max_length=20,
        required=False,
        validators=[sync_type_validator]
    )