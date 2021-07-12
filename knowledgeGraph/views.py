# -*- coding: utf-8 -*-
import os

from django.shortcuts import render
from django.http import JsonResponse
from knowledgeGraph import createGraph
from knowledgeGraph.langconv import *
from knowledgeGraph import models
from knowledgeGraph import csv2list
import random


# Create your views here.


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


def query(request):
    if request.method == 'POST':
        name = request.POST.get('Node')
        source = request.POST.get('Source')
        status = createGraph.structure(name, source, 3)
        # status = 'YES'
        print('Node:', name)
        print('status:', status)
        return JsonResponse({'status': status}, safe=False)
    return render(request, 'query.html')


def examination(request):
    data_path = os.path.dirname(os.path.dirname(__file__))
    SingleChoiceQuestions, MultipleChoiceQuestions, TureFalseQuestions = csv2list.getExam(data_path)
    return render(request, 'examination.html',
                  {'SingleChoiceQuestions': random.sample(list(SingleChoiceQuestions), 10),
                   'MultipleChoiceQuestions': random.sample(list(MultipleChoiceQuestions), 5),
                   'TureFalseQuestions': random.sample(list(TureFalseQuestions), 5)})
