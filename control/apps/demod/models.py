# coding=utf-8
from django.db import models

from control.apps.modu.models import BaseModel
from control.control.base import getLogger

logger = getLogger(__name__)


class DemodModelManager(models.Manager):
    def create(self,
               signal_id,
               ant_type,
               protocol,
               sync_type):
        try:
            demod_model = DemodModel(signal_id=signal_id,
                                 ant_type=ant_type,
                                 protocol=protocol,
                                 sync_type=sync_type)
            demod_model.save()
            return demod_model, None
        except Exception as exp:
            logger.error("demod save error: %s" % exp)
            return None, exp


class DemodModel(BaseModel):
    class Meta:
        db_table = 'demod'
    signal_id = models.CharField(
        max_length=20,
        null=False,
        unique=False
    )

    ant_type = models.CharField(
        max_length=20,
        null=False,
        unique=False
    )

    protocol = models.CharField(
        max_length=20,
        null=False,
        unique=False
    )

    sync_type = models.CharField(
        max_length=20,
        null=False,
        unique=False
    )

    objects = DemodModelManager()

    @classmethod
    def demod_exist_by_id(cls, signal_id, deleted=False):
        """
        验证demod_model 是否存在
        :param signal_id:
        :return:
        """
        try:
            return DemodModel.objects.filter(deleted=deleted).filter(signal_id=signal_id).exists()
        except Exception as exp:
            logger.error("demod save error: %s" % exp)
            return False

    @classmethod
    def demod_delete_by_id(self, signal_id, deleted=False):
        """
        删除数据表内容
        :param signal_id:
        :param deleted:
        :return:
        """
        try:
            return DemodModel.objects.filter(deleted=deleted).filter(signal_id=signal_id).delete()
        except Exception as exp:
            logger.error("demod delete error: %s" % exp)
            return False