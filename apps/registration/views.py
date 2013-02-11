# -*- coding: utf-8 -*-
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from apps.registration.forms import RegisterForm

from apps.registration.models import RegistrationProfile
from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

# 老的注册的方法,在form里完成的业务逻辑,后来加上发送邮件等业务,用户持久化就移到view里了
# def sign_up(request):
#     """
#     用户登录了不能重复注册,邮箱添加验证
#     """
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             return HttpResponseRedirect("/")
#     else:
#         form = RegisterForm()
#         # 注册的form添加
#     return render_to_response("registration/sign_up.html", 
#         {'form': form,},
#         context_instance=RequestContext(request))

# 激活用户
def activate(request,
             template_name='registration/activate.html',
             success_url=None, extra_context=None, **kwargs):
    # 从激活码激活用户,并返回用户
    account = activate_by_key(request, **kwargs)
    # 如果成功激活用户 
    if account:
        if success_url is None:
            to, args, kwargs = post_activation_redirect(request, account)
            return redirect(to, *args, **kwargs)
        else:
            # 如果配置了返回页面的话
            return redirect(success_url)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    # 额外的变量添加的请求的上下文
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              kwargs,
                              context_instance=context)


def register(request, success_url=None, form_class=None,
             disallowed_url='registration_disallowed',
             template_name='registration/registration_form.html',
             extra_context=None):

    # 先判断是否允许注册
    if not registration_allowed(request):
    # 不允许注册的时候,直接返回一个url
        return redirect(disallowed_url)
    if form_class is None:
        form_class = get_form_class(request)

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = register_user(request, **form.cleaned_data)
            if success_url is None:
                to, args, kwargs = post_registration_redirect(request, new_user)
                return redirect(to, *args, **kwargs)
            else:
                return redirect(success_url)
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)
# 注册用户,发送邮件等业务,调用model里的ManageModel的方法完成
def register_user(request, **kwargs):
    username, email, password = kwargs['username'], kwargs['email'], kwargs['password1']
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)
    new_user = RegistrationProfile.objects.create_inactive_user(username, email,
                                                                password, site)
    return new_user
# 以验证码激活用户
def activate_by_key(request, activation_key):
    activated = RegistrationProfile.objects.activate_user(activation_key)
    return activated
# 是否允许注册,从settings里拿参数
def registration_allowed(request):
    return getattr(settings, 'REGISTRATION_OPEN', True)

def get_form_class(request):
    return RegisterForm
# 注册返回页面,默认值的返回
def post_registration_redirect(request, user):
    return ('registration_complete', (), {})
# 激活返回页面,默认值的返回
def post_activation_redirect(request, user):
    return ('registration_activation_complete', (), {})