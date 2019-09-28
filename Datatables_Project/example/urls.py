# !/usr/bin/env python3
# encoding: utf-8
"""
@version: 0.1
@author: Jack
@license: Apache Licence
@contact: hfutbj233@163.com
@software: PyCharm
@file: urls.py
@time: 2019/9/18 20:29
"""
from django.urls import path
from . import views
app_name = 'example'

urlpatterns = [
    path('', views.index, name='index'),
    path('initial_database', views.initial_database, name='initial_database'),
    path('basic_tables', views.get_basic_tables, name='basic_tables'),
    path('ajax_tables', views.use_ajax_tables, name='ajax_tables'),
    path('request_ajax', views.request_ajax, name='request_ajax'),
    path('backend_tables', views.slice_in_backend_tables, name='backend_tables'),
    path('request_backend', views.request_backend, name='request_backend'),
]
