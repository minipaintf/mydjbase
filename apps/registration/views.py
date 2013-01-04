# -*- coding: utf-8 -*-
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from apps.registration.forms import RegisterForm

def sign_up(request):
    """
    用户登录了不能重复注册,邮箱添加验证
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = RegisterForm()
        # 注册的form添加
    return render_to_response("registration/sign_up.html", 
        {'form': form,},
        context_instance=RequestContext(request))