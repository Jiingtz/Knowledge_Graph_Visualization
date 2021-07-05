from django.db import models


# Create your models here.

class BriefIntroduction(models.Model):
    # 简介表
    name = models.CharField(max_length=64)  # 知识点名称
    introduction = models.CharField(max_length=1000)  # 介绍
    link = models.CharField(max_length=200)  # 链接
