# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _



class UCmember(models.Model):
    """存储和ucenter对接的用户数据"""
    uid = models.IntegerField('discuz member uid')
    username = models.CharField('discuz member username', max_length=30)
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    created_date = models.DateTimeField('date created')
    updated_date = models.DateTimeField('date updated')