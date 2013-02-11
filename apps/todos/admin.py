# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.todos.models import Todo

class TodoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Date Created at', {'fields': ['created_date']}),
        ('Date updated at', {'fields': ['updated_date']}),
    ]
    list_display = ('created_date', 'updated_date')

admin.site.register(Todo,TodoAdmin)