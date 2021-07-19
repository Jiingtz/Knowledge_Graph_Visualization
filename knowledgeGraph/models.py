from django.db import models


# Create your models here.

# 知识点简介表
class BriefIntroduction(models.Model):
    name = models.CharField(max_length=64)  # 知识点名称
    introduction = models.CharField(max_length=1000)  # 介绍
    link = models.CharField(max_length=200)  # 链接


# 用户历史行为
class UserHistoryBehavior(models.Model):
    username = models.CharField(max_length=64)  # 用户名
    answer_time = models.DateTimeField()  # 做题时间
    wrong_single_num = models.IntegerField()  # 单选题错题数量
    single_score = models.IntegerField()  # 单选题得分

    wrong_tf_num = models.IntegerField()  # 判断题错题数量
    tf_score = models.IntegerField()  # 判断题得分

    wrong_mul_num = models.IntegerField()  # 多选题错题数量
    mul_score = models.IntegerField()  # 多选题得分

    wrong_num = models.IntegerField()  # 总错题数
    score = models.IntegerField()  # 总得分
    wrong_knowledge_points = models.TextField()  # 错误知识点


# 用户错误（薄弱）知识点次数表
class WrongKnowledgeNum(models.Model):
    knowledgeName = models.CharField(max_length=64)  # 错误知识点名称
    knowledgeID = models.CharField(max_length=64)  # 错误知识点ID
    WrongNum = models.IntegerField()  # 错误次数
    username = models.CharField(max_length=64)  # 用户名
