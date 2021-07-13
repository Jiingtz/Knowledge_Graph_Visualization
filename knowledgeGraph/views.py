# -*- coding: utf-8 -*-
import os

from django.shortcuts import render, redirect
from django.http import JsonResponse
from functools import wraps

from django.urls import reverse

from knowledgeGraph import createGraph
from knowledgeGraph.langconv import *
from knowledgeGraph import models
from knowledgeGraph import csv2list
from knowledgeGraph import baike
import random


# Create your views here.

# 判断是否登录
def login_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        print(request.COOKIES)
        is_login = request.COOKIES.get('is_login')
        if is_login != '1':
            return redirect('/login/?url={}'.format(request.path_info))
        ret = func(request, *args, **kwargs)
        return ret

    return inner


def login(request):
    if request.method == 'POST':
        userEmail = request.POST.get('login_email')
        userPw = request.POST.get('login_pw')
        if userEmail == 'ztj@qq.com' and userPw == '123456':
            url = request.GET.get('url')
            if url:
                return_url = url
            else:
                return_url = reverse('index')
            ret = redirect(return_url)
            ret.set_cookie('is_login', '1')
            return ret
        else:
            error = '邮箱或密码错误'
    return render(request, 'login.html', locals())


def index(request):
    if request.method == 'POST':
        nodeName = request.POST.get('nodeName')
        nodeName = Converter('zh-hans').convert(nodeName)  # 繁体字转化
        nodeName.encode('utf-8')
        ret = models.BriefIntroduction.objects.filter(name=nodeName)
        if ret:
            introduction = ret[0].introduction
            link = ret[0].link
        else:
            introduction = "尚未收录词条：" + nodeName
            link = 'https://baike.baidu.com/'
        print(nodeName)
        print(introduction)
        return JsonResponse({'introduction': introduction, 'link': link}, safe=False)
    return render(request, 'index.html')


@login_required
def query(request):
    if request.method == 'POST':
        name = request.POST.get('Node')
        source = request.POST.get('Source')
        status = createGraph.structure(name, source, 2)
        print('Node:', name)
        print('status:', status)
        return JsonResponse({'status': status}, safe=False)
    return render(request, 'query.html')


@login_required
def examination(request):
    data_path = os.path.dirname(os.path.dirname(__file__))
    SingleChoiceQuestions, MultipleChoiceQuestions, TureFalseQuestions = csv2list.getExam(data_path)
    return render(request, 'examination.html',
                  {'SingleChoiceQuestions': random.sample(list(SingleChoiceQuestions), 10),
                   'MultipleChoiceQuestions': random.sample(list(MultipleChoiceQuestions), 5),
                   'TureFalseQuestions': random.sample(list(TureFalseQuestions), 5)})
