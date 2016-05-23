# coding=utf-8

from .validator import *
from control.control.logger import getLogger
logger = getLogger(__name__)

class CreateSignalSerializer(serializers.Serializer):
    """
    创建信号
    """

    filename = serializers.CharField(
        max_length=20,
        required=True,
        validators=[]
    )

    packagenum = serializers.IntegerField(
        required=False,
        validators=[packagenum_validator]
    )

    action_all = serializers.BooleanField(
        required=False,
        validators=[action_all_validator]
    )

    action = serializers.CharField(
        max_length=20,
        required=False,
        validators=[action_validator]
    )

    distri_id = serializers.CharField(
        required=False,
        max_length=20,
        validators=[distri_id_validator]
    )

    partable_id = serializers.CharField(
        required=False,
        max_length=20,
        validators=[partable_id_validator]
    )

    timetable_id = serializers.CharField(
        required=False,
        max_length=20,
        validators=[timetable_id_validator]
    )

    aisdata_id = serializers.CharField(
        required=False,
        max_length=20,
        validators=[aisdata_id_validator]
    )
    # logger.info("aisdata_id is %s"% aisdata_id)
    singal_id = serializers.CharField(
        required=False,
        max_length=20,
        validators=[signal_id_validator]
    )


    lon = serializers.FloatField(
        required=False,
        validators=[lon_validator]
    )

    lat = serializers.FloatField(
        required=False,
        validators=[lat_validator]
    )

    height = serializers.IntegerField(
        required=False,
        validators=[height_validator]
    )

    vesnum = serializers.IntegerField(
        required=False,
        validators=[vesnum_validator]
    )

    obtime = serializers.IntegerField(
        required=False,
        validators=[obtime_validator]
    )

    distri_mode = serializers.CharField(
        required=False,
        validators=[distri_mode_validator]
    )

    ant_pitch = serializers.IntegerField(
        required=False,
        validators=[ant_pitch_validator]
    )

    ant_azimuth = serializers.FloatField(
        required=False,
        validators=[ant_azimuth_validator]
    )

    ant_type = serializers.CharField(
        required=False,
        validators=[ant_type_validator]
    )

    channel_type = serializers.CharField(
        required=False,
        validators=[channel_type_validator]
    )

    protocol = serializers.CharField(
        required=False,
        validators=[protocol_validator]
    )

    snr = serializers.IntegerField(
        required=False,
        validators=[snr_validator]
    )