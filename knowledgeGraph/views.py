# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from knowledgeGraph import Neo4j_Model
from knowledgeGraph import createGraph


# Create your views here.

def index(request):
    if request.method == 'POST':
        nodeName = request.POST.get('nodeName')
        print(nodeName)
        introduction = '喜欢吗？'
        return JsonResponse({'introduction': introduction}, safe=False)
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
