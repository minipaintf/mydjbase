# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# 注册的表单
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","email")
    email = forms.EmailField(max_length=75)

    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        # 这个是自己添加的
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # 默认没有激活
        user.is_active = False
        if commit:
            user.save()
        return user