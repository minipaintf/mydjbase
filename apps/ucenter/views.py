# -*- coding: utf-8 -*-
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from firstp import settings


def uc_php(request):
    """
    通信接口 访问路径为/api/uc.php
    接口接受一个get请求,参数为编码后的code
    """
    # 解析code
    code = request.REQUEST.get('code','')
    print settings.API_KEY
    return HttpResponse("1")