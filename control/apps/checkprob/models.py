# coding=utf-8
from django.db import models

from control.apps.modu.models import BaseModel
from control.control.base import getLogger

logger = getLogger(__name__)

class CheckProbModelManager(models.Manager):
    def create(self, action, demodSignal_id):
        try:
            checkprob_model = CheckProbModel(action=action,
                                             demodSignal_id=demodSignal_id)
            checkprob_model.save()
            return checkprob_model, None
        except Exception as exp:
            logger.error("demod save error: %s" % exp)
            return None, exp


class CheckProbModel(BaseModel):
    class Meta:
        db_table = 'checkprob'
    demodSignal_id = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )

    objects = CheckProbModelManager()

    @classmethod
    def demod_exist_by_id(cls, demodSignal_id, deleted=False):
        """
        验证checkprob_model 是否存在
        :param signal_id:
        :return:
        """
        try:
            return CheckProbModel.objects.filter(deleted=deleted).filter(demodSignal_id=demodSignal_id).exists()
        except Exception as exp:
            logger.error("demod save error: %s" % exp)
            return False
    @classmethod
    def demod_delete_by_id(self, demodSignal_id, deleted=False):
        """
        删除数据表内容
        :param signal_id:
        :param deleted:
        :return:
        """
        try:
            return CheckProbModel.objects.filter(deleted=deleted).filter(demodSignal_id=demodSignal_id).delete()
        except Exception as exp:
            logger.error("demod delete error: %s" % exp)
            return exp