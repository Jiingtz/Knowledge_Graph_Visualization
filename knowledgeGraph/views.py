# -*- coding: utf-8 -*-
import json
import os

from django.shortcuts import render, redirect
from django.http import JsonResponse
from functools import wraps

from django.urls import reverse

from knowledgeGraph import createGraph
from knowledgeGraph.langconv import *
from knowledgeGraph import models
from knowledgeGraph import csv2list
import random


# Create your views here.

# 判断是否登录
def login_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        print(request.COOKIES)
        is_login = request.get_signed_cookie('is_login', salt='s28', default='error')
        if is_login != '1':
            return redirect('/login/?url={}'.format(request.path_info))
        ret = func(request, *args, **kwargs)
        return ret

    return inner


# 注册
def register(request):
    if request.method == 'POST':
        user_name = request.POST.get('register_name')
        user_pwd = request.POST.get('register_pw')
        user_email = request.POST.get('register_email')
        models.UserInfo.objects.create(userName=user_name, userPassword=user_pwd, userEmail=user_email)
        return redirect('login')

    return render(request, 'login.html')


def check_username(request):
    username = request.GET.get('username')
    print()
    user = models.UserInfo.objects.filter(userName=username)
    if user:
        JsonResponse({'status': 'fail', 'msg': '此用户名已被占用'})
    else:
        JsonResponse({'status': 'success', 'msg': '此用户名可用'})


# 登录
def login(request):
    if request.method == 'POST':
        userEmail = request.POST.get('login_email')
        userPw = request.POST.get('login_pw')
        user = models.UserInfo.objects.filter(userEmail=userEmail, userPassword=userPw)
        if user:
            url = request.GET.get('url')
            if url:
                return_url = url
            else:
                return_url = reverse('index')
            ret = redirect(return_url)
            ret.set_signed_cookie('is_login', '1', salt='s28')
            return ret
        else:
            error = '邮箱或密码错误'
    return render(request, 'login.html', locals())


# 注销
def logout(request):
    ret = redirect('login')
    ret.delete_cookie('is_login')
    return ret


# 首页（3D展示页面）
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


# 知识图谱查询与创建
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


# 答题页面
@login_required
def examination(request):
    if request.method == 'POST':
        answer = json.loads(request.POST.get('answer'))
        single_answer = answer.get('single_answer')
        tf_answer = answer.get('tf_answer')
        mul_answer = answer.get('mul_answer')
        data_path = os.path.dirname(os.path.dirname(__file__))
        SingleChoiceQuestions, MultipleChoiceQuestions, TureFalseQuestions = csv2list.getExam(data_path)
        print(single_answer)
        print(tf_answer)
        print(mul_answer)
        # 单选题得分
        single_score = 0
        for key in single_answer:
            for s_c in SingleChoiceQuestions:
                if key == s_c[0]:
                    if single_answer[key].split('.')[0] == s_c[2]:
                        single_score += 5
        print('单选题得分：', single_score)
        # 判断题得分
        tf_score = 0
        for key in tf_answer:
            for s_c in TureFalseQuestions:
                if key == s_c[0]:
                    if tf_answer[key] == s_c[2]:
                        tf_score += 4
        print('判断题得分：', tf_score)
        # 多选题得分
        mul_score = 0
        for key in mul_answer:
            for s_c in MultipleChoiceQuestions:
                if key == s_c[0]:
                    if [i.split('.')[0] for i in mul_answer[key]] == s_c[2]:
                        mul_score += 6
        print('多选题得分：', mul_score)
        total_score = single_score + tf_score + mul_score
        print('总分：', total_score)
        return JsonResponse({'score': total_score}, safe=False)
    else:
        data_path = os.path.dirname(os.path.dirname(__file__))
        SingleChoiceQuestions, MultipleChoiceQuestions, TureFalseQuestions = csv2list.getExam(data_path)
        return render(request, 'examination.html',
                      {'SingleChoiceQuestions': random.sample(list(SingleChoiceQuestions), 10),
                       'MultipleChoiceQuestions': random.sample(list(MultipleChoiceQuestions), 5),
                       'TureFalseQuestions': random.sample(list(TureFalseQuestions), 5)})


# 知识点推荐页面
@login_required
def recommend(request):
    pass
