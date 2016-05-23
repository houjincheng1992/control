# coding=utf-8

import os
import string
import random
import time

from django.conf import settings
from django.contrib.auth.admin import User
from django.utils.translation import ugettext as _

from control.control.err_msg import PARAMETER_CODE
from control.control.logger import getLogger

logger = getLogger(__name__)


def user_temp():
    """
    get user_temp
    :return: user
    """
    try:
        user = User.objects.get(username="user-safoewfw")
        return user.username
    except Exception as exp:
        try:
            user = User.objects.create_user(username="user-safoewfw", email="234241213@qq.com", password="12edd23")
            return user.username
        except Exception as exp:
            logger.error("Create User Failed！")
            return False


def randomname_maker(num=settings.NAME_ID_LENGTH):
    words = string.digits + string.lowercase
    # number:zero,one; lower case: ok,lucky
    exclude_words = ['0', 'o', 'l', '1']
    words = ''.join(set(words) - set(exclude_words))
    random.seed(time.time())
    return ''.join(random.sample(words, num))


class get_path():
    """
    获取文件路径
    :return:
    """
    MATLAB_FILE_PATH = os.path.abspath(os.path.join("./AIS"))
    CELERY_PATH = os.path.abspath(os.path.join("../"))



def convert_to_string(data):
    """
    Convert dict/list to string by:
        geting the firt item of firt value
    """
    if isinstance(data, dict):
        return convert_to_string(data.values()[0])
    elif isinstance(data, list):
        return convert_to_string(data[0])
    elif not isinstance(data, basestring):
        return str(data)
    return data

def is_simple_string_list(data):
    """
    Check if data is a string list.
    """
    if not isinstance(data, list):
        return False

    for ret in data:
        if not isinstance(ret, basestring):
            return False

    return True

def get_code_by_parameter(parameter):
    """
    get code by parameter
    :param parameter:
    :return:
    """
    return PARAMETER_CODE.get(parameter)


def control_code(validator):
    """
    get code , msg
    :param validator:
    :return:
    """
    if not validator:
        return -1, ""
    errors = validator.errors
    if errors.keys():
        parameter = errors.keys()[0]
        msg = errors.get(parameter)[0]
        code = get_code_by_parameter(parameter)
        return code, msg
    else:
        return -1, ""


def control_response(code=0,
                     msg=_(u"服务器响应成功"),
                     total_count=0,
                     ret_set=None,
                     action_record=None,
                     ret_name_id=None, **kwargs):
    """
    generate return parameter
    :param code:  error code
    :param msg:  error message
    :param total_count: ret number
    :param ret_set: action_id
    :param action_record: action 记录
    :param ret_name_id: action_id_name
    :param kwargs: more arguments
    :return: return parameter dict
    """
    msg = convert_to_string(msg)

    if code == 0:
        parameter_msg = _(u"服务器响应成功")
    else:
        parameter_msg = _(u"服务器响应失败")

    ret = {"ret_code": code, "msg": msg}
    ret["ret_msg"] = parameter_msg  # temp msg

    if code == 0 or total_count != 0:
        ret["total_count"] = total_count
        ret["ret_set"] = ret_set or []

    ret["ret_name_id"] = ret_name_id

    if action_record is not None:
        if is_simple_string_list(action_record):
            action_record = ','.join(action_record)
        ret["action_record"] = action_record
    ret.update(kwargs)

    return ret
