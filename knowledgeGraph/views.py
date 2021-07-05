# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from knowledgeGraph import createGraph
from knowledgeGraph.langconv import *
from knowledgeGraph import models


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


def relationship(request):
    return render(request, 'relationship.html')
