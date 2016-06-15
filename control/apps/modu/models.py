# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from control.control.logger import getLogger
logger = getLogger(__name__)

# Create your models here.

DISTRI_MODEL_CHOICE = (
    ("default", _("default")),
    ("random", _("random")),
    ("fact", _("fact"))
)

ANTENNA_CHOICE = (
    ("default", _("default")),
    ("yagi", _("yagi"))
)

CHANNEL_CHOICE = (
    ("default", _("default")),
    ("free space loss", _("free space loss"))
)

SLOT_SELECT_CHOICE = (
    ("default", _("default")),
    ("SOTDMA", _("SOTDMA"))
)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    # create datetime
    create_datetime = models.DateTimeField(
        auto_now_add=True
    )
    # deleted
    deleted = models.BooleanField(
        default=False
    )
    # deleted datetime
    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # file size
    signal_size = models.FloatField(
        null=True,
        blank=True,
        default=0
    )

    schedule = models.FloatField(
        null=True,
        blank=True,
        default=0
    )


class DistriManager(models.Manager):
    def create(self,
               user,
               distri_id,
               distri_lon,
               distri_lat,
               distri_height,
               distri_ves_num,
               distri_mode):
        try:
            user = User.objects.get(username=user)
            distri_model = DistriModel(user=user,
                                       distri_id=distri_id,
                                       distri_lon=distri_lon,
                                       distri_lat=distri_lat,
                                       distri_height=distri_height,
                                       distri_ves_num=distri_ves_num,
                                       distri_mode=distri_mode)
            distri_model.save()
            return distri_model, None
        except Exception as exp:
            return None, exp


class PartableModelManager(models.Manager):
    def create(self,
               partable_id,
               distri_id,
               pitch,
               azimuth,
               antenna_type,
               channel_type):
        try:
            distri = DistriModel.get_distri_by_id(distri_id)
            partable_model = PartableModel(distri=distri,
                                           partable_id=partable_id,
                                           pitch=pitch,
                                           azimuth=azimuth,
                                           antenna_type=antenna_type,
                                           channel_type=channel_type
                                           )
            partable_model.save()
            return partable_model, None
        except Exception as exp:
            return None, exp


class TimetableModelManager(models.Manager):
    def create(self,
               distri_id,
               partable_id,
               timetable_id,
               obtime,
               transinterval,
               protocol):
        try:
            distri = DistriModel.get_distri_by_id(distri_id)
            partable = PartableModel.get_partbale_by_id(partable_id)
            timetable_model = TimetableModel(distri=distri,
                                             partable=partable,
                                             timetable_id=timetable_id,
                                             obtime=obtime,
                                             transinterval=transinterval,
                                             protocol=protocol
                                             )
            timetable_model.save()
            return timetable_model, None
        except Exception as exp:
            return None, exp


class AisdataModelManager(models.Manager):
    def create(self,
                distri_id,
                timetable_id,
                aisdata_id
                ):
        try:
            distri = DistriModel.get_distri_by_id(distri_id)
            timetable = TimetableModel.get_timetable_by_id(timetable_id)
            aisdata_model = AisdataModel(distri=distri,
                                         timetable=timetable,
                                         aisdata_id=aisdata_id)
            aisdata_model.save()
            return aisdata_model, None
        except Exception as exp:
            return None, exp


class SignalModelManager(models.Manager):
    def create(self,
               name_signal,
               partable_id,
               timetable_id,
               aisdata_id,
               signal_id,
               snr):
        try:
            partable = PartableModel.get_partbale_by_id(partable_id)
            timetable = TimetableModel.get_timetable_by_id(timetable_id)
            aisdata = AisdataModel.get_aisdata_by_id(aisdata_id)
            signal_model = SignalModel(name_signal=name_signal,
                                       partable=partable,
                                       timetable=timetable,
                                       aisdata=aisdata,
                                       signal_id=signal_id,
                                       snr=snr
                                       )
            signal_model.save()
            return signal_model, None
        except Exception as exp:
            return None, exp


# class AISUser(User):
#     class Meta:
#         db_table = "AISUser"


class DistriModel(BaseModel):
    class Meta:
        db_table = "distri"
    # distri owner
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT)

    # user = models.CharField(
    #     max_length=20,
    #     null=False,
    #     unique=False)
    # distri id
    distri_id = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )
    # distri lon
    distri_lon = models.FloatField(
        null=False,
        default=0
    )

    # distri lat
    distri_lat = models.FloatField(
        null=False,
        default=0
    )

    # distri height
    distri_height = models.IntegerField(
        null=False,
        default=0
    )

    # distri ves num
    distri_ves_num = models.IntegerField(
        null=False,
        default=0
    )

    # distri mode
    distri_mode = models.CharField(
        max_length=20,
        null=False,
        choices=DISTRI_MODEL_CHOICE
    )

    # manager
    objects = DistriManager()

    @classmethod
    def distri_exist_by_id(cls, distri_id, deleted=False):
        try:
            return DistriModel.objects.filter(deleted=deleted).filter(distri_id=distri_id).exists()
        except Exception as exp:
            logger.error("exist distri_id error: %s" % str(exp))
            return False

    @classmethod
    def get_distri_by_id(cls, distri_id, deleted=False):
        try:
            return DistriModel.objects.filter(deleted=deleted).get(distri_id=distri_id)
        except Exception as exp:
            logger.error("get distri error is :%s" % exp)
            return False

    @classmethod
    def distri_delete_by_id(cls, distri_id, deleted = False):
        try:
            return DistriModel.objects.get(distri_id=distri_id).delete()
        except Exception as exp:
            logger.error("delete distri error: %s" % str(exp))
            return False

class PartableModel(BaseModel):
    class Meta:
        db_table = "partable"

    # partable from
    distri = models.ForeignKey(DistriModel,
                               on_delete=models.PROTECT)

    # partable id
    partable_id = models.CharField(
        max_length=30,
        null=False,
        unique=True
    )


    # antenna 偏移的俯仰角
    pitch = models.FloatField(null=False,
                              default=0)

    # antenna 偏移的方位角
    azimuth = models.FloatField(null=False,
                                default=0)
    # antenna 类型
    antenna_type = models.CharField(
        max_length=20,
        null=False,
        choices=ANTENNA_CHOICE
    )

    # channel 类型
    channel_type = models.CharField(
        max_length=20,
        null=False,
        choices=CHANNEL_CHOICE
    )

    objects = PartableModelManager()

    @classmethod
    def partable_exist_by_id(cls, partable_id, deleted=False):
        try:
            return PartableModel.objects.filter(deleted=deleted).filter(partable_id=partable_id).exists()
        except Exception as exp:
            logger.error("exist partable error: %s" % str(exp))
            return False

    @classmethod
    def get_partbale_by_id(cls, partable_id, deleted=False):
        try:
            return PartableModel.objects.filter(deleted=deleted).get(partable_id=partable_id)
        except Exception as exp:
            logger.error("get partable_id error : %s" % str(exp))
            return False

    @classmethod
    def get_distri_id_by_partable_id(cls, partable_id, deleted = False):
        try:
            distri = PartableModel.objects.filter(deleted=deleted).get(partable_id=partable_id).distri
            return distri.distri_id
        except Exception as exp:
            logger.error("get distri_id error: %s" % str(exp))
            return False

    @classmethod
    def partable_delete_by_id(cls, partable_id, deleted = False):
        try:
            return PartableModel.objects.filter(deleted=deleted).get(partable_id=partable_id).delete()
        except Exception as exp:
            logger.error("delete partable error: %s" % str(exp))
            return False

class TimetableModel(BaseModel):
    class Meta:
        db_table = "timetable"

    distri = models.ForeignKey(DistriModel,
                               on_delete=models.PROTECT)

    partable = models.ForeignKey(PartableModel,
                                 on_delete=models.PROTECT)

    timetable_id = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )

    transinterval = models.IntegerField(
        null=False,
        default=0
    )

    obtime = models.FloatField(null=False,
                               default=0)

    # 选择分配时隙的协议
    protocol = models.CharField(
        max_length=20,
        null=False,
        choices=SLOT_SELECT_CHOICE
    )

    objects = TimetableModelManager()

    @classmethod
    def timetable_exist_by_id(cls, timetable_id, deleted=False):
        try:
            return TimetableModel.objects.filter(deleted=deleted).filter(timetable_id=timetable_id).exists()
        except Exception as exp:
            logger.error("exist timetable error: %s" % str(exp))
            return False

    @classmethod
    def get_timetable_by_id(cls, timetable_id, deleted=False):
        try:
            return TimetableModel.objects.filter(deleted=deleted).get(timetable_id = timetable_id)
        except Exception as exp:
            logger.error("get timetable error: %s" % str(exp))
            return False

    @classmethod
    def get_distri_id_by_timetable_id(cls, timetable_id, deleted = False):
        try:
            distri = TimetableModel.objects.filter(deleted=deleted).get(timetable_id=timetable_id).distri
            return distri.distri_id
        except Exception as exp:
            logger.error("get distri_id error: %s" % str(exp))
            return False

    @classmethod
    def get_partable_id_by_timetable_id(cls, timetable_id, deleted = False):
        try:
            partable = TimetableModel.objects.filter(deleted=deleted).get(timetable_id=timetable_id).partable
            return partable.partable_id
        except Exception as exp:
            logger.error("get partable_id error: %s" % str(exp))
            return False

    @classmethod
    def timetable_delete_by_id(cls, timetable_id, deleted = False):
        try:
            return TimetableModel.objects.filter(deleted=deleted).get(timetable_id=timetable_id).delete()
        except Exception as exp:
            logger.error("delete timetable error: %s" % str(exp))
            return False


class AisdataModel(BaseModel):
    class Meta:
        db_table = "aisdata"
    distri = models.ForeignKey(DistriModel,
                               on_delete=models.PROTECT)
    timetable = models.ForeignKey(TimetableModel,
                                  on_delete=models.PROTECT)
    # aisdata id
    aisdata_id = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )
    # manager

    objects = AisdataModelManager()

    @classmethod
    def aisdata_exist_by_id(cls, aisdata_id, deleted=False):
        try:
            return AisdataModel.objects.filter(deleted=deleted).filter(aisdata_id=aisdata_id).exists()
        except Exception as exp:
            logger.error("exist aisdata error: %s" % str(exp))
            return False

    @classmethod
    def get_aisdata_by_id(cls, aisdata_id, deleted=False):
        try:
            return AisdataModel.objects.filter(deleted=deleted).get(aisdata_id=aisdata_id)
        except Exception as exp:
            logger.error("get aisdata error: %s" % str(exp))
            return False

    @classmethod
    def get_distri_id_by_aisdata_id(cls, aisdata_id, deleted = False):
        try:
            distri = AisdataModel.objects.filter(deleted=deleted).get(aisdata_id=aisdata_id).distri
            return distri.distri_id
        except Exception as exp:
            logger.error("get distri_id error: %s" % str(exp))
            return False

    @classmethod
    def get_timetable_id_by_aisdata_id(cls, aisdata_id, deleted = False):
        try:
            timetable = AisdataModel.objects.filter(deleted=deleted).get(aisdata_id=aisdata_id).timetable
            return timetable.timetable_id
        except Exception as exp:
            logger.error("get timetable_id error: %s" % str(exp))
            return False

    @classmethod
    def aisdata_delete_by_id(cls, aisdata_id, deleted = False):
        try:
            return AisdataModel.objects.filter(deleted=deleted).get(aisdata_id=aisdata_id).delete()
        except Exception as exp:
            logger.error("delete aisdata error: %s" % str(exp))
            return False

    # @classmethod
    # def get_aisdataid_by_id(cls, signal_id, deleted = False):
    #     try:
    #         aisdata = SignalModel.objects.filter(deleted=deleted).get(signal_id=signal_id).aisdata
    #         return aisdata.aisdata_id
    #     except Exception as exp:
    #         logger.error("get aisdata_id error: %s" % str(exp))
    #         return False

class SignalModel(BaseModel):
    class Meta:
        db_table = "aissignal"
    partable = models.ForeignKey(PartableModel,
                                 on_delete=models.PROTECT)
    timetable = models.ForeignKey(TimetableModel,
                                 on_delete=models.PROTECT)
    aisdata = models.ForeignKey(AisdataModel,
                                 on_delete=models.PROTECT)

    # signal id
    signal_id = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )

    name_signal = models.CharField(
        max_length=30,
        null=False,
        unique=False
    )

    snr = models.IntegerField(null=False)

    objects = SignalModelManager()

    @classmethod
    def signal_exist_by_id(cls, signal_id, deleted=False):
        try:
            return SignalModel.objects.filter(deleted=deleted).filter(signal_id=signal_id).exists()
        except Exception as exp:
            logger.error("exist signal error: %s" % str(exp))
            return False

    @classmethod
    def signal_exist_by_name_signal(cls, name_signal, deleted=False):
        try:
            return SignalModel.objects.filter(deleted=deleted).filter(filename=name_signal).exists()
        except Exception as exp:
            logger.error("exist signal error: %s" % str(exp))
            return False

    @classmethod
    def get_signal_by_id(cls, signal_id, deleted=False):
        try:
            return SignalModel.objects.filter(deleted=deleted).get(signal_id=signal_id)
        except Exception as exp:
            logger.error("get signal error: %s" % str(exp))
            return False

    @classmethod
    def get_signal_by_name_signal(cls, name_signal, deleted=False):
        try:
            return SignalModel.objects.filter(deleted=deleted).get(name_signal=name_signal)
        except Exception as exp:
            logger.error("get signal by name_signal error: %s" % str(exp))
            return False

    @classmethod
    def get_aisdata_id_by_siganl_id(cls, signal_id, deleted=False):
        try:
            aisdata = SignalModel.objects.filter(deleted=deleted).get(signal_id=signal_id).aisdata
            return aisdata.aisdata_id
        except Exception as exp:
            logger.error("get aisdata_id error: %s" % str(exp))
            return False

    @classmethod
    def get_timetable_id_by_signal_id(cls, signal_id, deleted = False):
        try:
            time_table = SignalModel.objects.filter(deleted=deleted).get(signal_id=signal_id).timetable
            return time_table.timetable_id
        except Exception as exp:
            logger.error("get timetable_id error: %s" % str(exp))
            return False

    @classmethod
    def get_partable_id_by_signal_id(cls, signal_id, deleted = False):
        try:
            par_table = SignalModel.objects.filter(deleted=deleted).get(signal_id=signal_id).partable
            return par_table.partable_id
        except Exception as exp:
            logger.error("get timetable_id error: %s" % str(exp))
            return False

    @classmethod
    def signal_delete_by_id(cls, signal_id, deleted = False):
        try:
            return SignalModel.objects.filter(deleted=deleted).get(signal_id=signal_id).delete()
        except Exception as exp:
            logger.error("delete signal error: %s" % str(exp))
            return False

    @classmethod
    def signal_get_record(cls, deleted=False):
        try:
            return SignalModel.objects.filter(deleted=deleted)
        except Exception as exp:
            logger.error("get signal record error: %s" % str(exp))
            return False

    @classmethod
    def status_size_save(cls, signal_id, signalsize, deleted=False):
        """
        :param signal_id:
        :param signalsize:
        :param schedule:
        :return:
        """
        try:
            signal = SignalModel.objects.filter(deleted=deleted).get(signal_id=signal_id)
            signal.signal_size = signalsize
            signal.save()
            return signal, None
        except Exception as exp:
            logger.error("siganlsize save error: %s" % str(exp))
            return None, exp


    @classmethod
    def status_schedule_save(cls, signal_id, schedule, deleted=False):
        """
        :param signal_id:
        :param signalsize:
        :param schedule:
        :return:
        """
        try:
            signal = SignalModel.objects.filter(deleted=deleted).get(signal_id=signal_id)
            signal.schedule = schedule
            signal.save()
            return signal, None
        except Exception as exp:
            logger.error("schedule save error: %s" % str(exp))
            return None, exp


class ScheduleModel(models.Model):
    class Meta:
        db_table = "schedule"
    model_id = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )

    model_rate = models.FloatField(
        null=False,
        unique=False
    )

    deleted = models.BooleanField(
        default=False
    )

    @classmethod
    def get_schedule_by_model_id(cls, model_id, deleted=False):
        """
        获取进度值
        :return:
        """
        try:
            logger.info("here!")
            logger.info("schedule is %s" % ScheduleModel.objects.get(model_id=model_id).model_rate)
            schedule = ScheduleModel.objects.filter(deleted=deleted).get(model_id=model_id).model_rate
            logger.info("schedule is %f" % schedule)
            return schedule
        except Exception as exp:
            return 0
