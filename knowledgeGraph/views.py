# -*- coding: utf-8 -*-
from django.shortcuts import render
from knowledgeGraph import Neo4j_Model


# Create your views here.

def index(request):
    return render(request, 'index.html')


def query(request):
    return render(request, 'query.html')


def relationship(request):
    return render(request, 'relationship.html')
