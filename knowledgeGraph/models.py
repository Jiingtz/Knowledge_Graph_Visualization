from django.db import models


# Create your models here.

# 知识点简介表
class BriefIntroduction(models.Model):
    name = models.CharField(max_length=64)  # 知识点名称
    introduction = models.CharField(max_length=1000)  # 介绍
    link = models.CharField(max_length=200)  # 链接


# 用户信息表
class UserInfo(models.Model):
    userName = models.CharField(max_length=64, unique=True)  # 用户名
    userEmail = models.EmailField(unique=True)  # 邮箱
    userPassword = models.CharField(max_length=64)  # 密码
