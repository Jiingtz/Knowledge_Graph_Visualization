# -*- coding: utf-8 -*-
import json
import os

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from functools import wraps

from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from knowledgeGraph import createGraph
from knowledgeGraph.langconv import *
from knowledgeGraph import models
from knowledgeGraph import csv2list
from knowledgeGraph import recommend_nodes
from knowledgeGraph import list2ques
from knowledgeGraph import kg_name2json
import random
import datetime


# Create your views here.

# # 判断是否登录
# def login_required(func):
#     @wraps(func)
#     def inner(request, *args, **kwargs):
#         # print(request.COOKIES)
#         is_login = request.get_signed_cookie('is_login', salt='s28', default='error')
#         if is_login != '1':
#             return redirect('/login/?next={}'.format(request.path_info))
#         ret = func(request, *args, **kwargs)
#         return ret
#
#     return inner
#

# 注册
def register(request):
    if request.method == 'POST':
        user_name = request.POST.get('register_name')
        user_pwd = request.POST.get('register_pw')
        user_email = request.POST.get('register_email')
        User.objects.create_user(username=user_name, password=user_pwd, email=user_email)
        return redirect('login')

    return render(request, 'login.html')


# 注册前检查用户名是否被占用
def check_username(request):
    username = request.GET.get('username')
    print(username)
    user = User.objects.filter(username=username)
    if user:
        return JsonResponse({'status': 'fail', 'msg': '此用户名已被占用'})
    else:
        return JsonResponse({'status': 'success', 'msg': '此用户名可用'})


# 登录
def login(request):
    if request.method == 'POST':
        status = 0
        userEmail = request.POST.get('login_email')
        userPw = request.POST.get('login_pw')
        if '@' in userEmail:
            username = User.objects.filter(email=userEmail)[0].username
            user = auth.authenticate(username=username, password=userPw)
        else:
            user = auth.authenticate(username=userEmail, password=userPw)
        if user:
            url = request.GET.get('next')
            auth.login(request, user)
            if url:
                return_url = url
            else:
                return_url = reverse('index')
            ret = redirect(return_url)
            # ret.set_signed_cookie('is_login', '1', salt='s28', max_age=60 * 60 * 24)
            status = 1
            return ret
        else:
            error = '用户名或密码错误'
            return render(request, 'login.html', {'status': status})
    return render(request, 'login.html')


# 注销
def logout(request):
    ret = redirect('login')
    ret.delete_cookie('is_login')
    auth.logout(request)
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
    else:
        if request.user.username:
            return render(request, 'index.html')
        else:
            user = auth.authenticate(username='jingluo', password=123456)
            auth.login(request, user)
            return render(request, 'index.html')


# 知识图谱查询与创建
@login_required
def query(request):
    if request.method == 'POST':
        name = request.POST.get('Node')
        source = request.POST.get('Source')
        depth = int(request.POST.get('Depth')) + 1
        status = createGraph.structure(name, source, depth)
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
        now_time = datetime.datetime.now()
        answer_time = now_time.strftime("%Y-%m-%d %H:%M")
        print('做题时间：', answer_time)
        print(single_answer)
        print(tf_answer)
        print(mul_answer)
        # 查看错题
        check_wrong_answer = []

        # 错误知识点ID eg:[['ITR5-1'], ['IBTP3-3-2'], ['IC4-4-1', 'ICN5-3-1', 'ICN5-2-1']
        wrong_knowledge_id = []
        # 错误知识点名称
        wrong_knowledge_name = []

        # 单选题得分
        single_score = 0
        # 单选题错题数
        wrong_single_num = 0
        for key in single_answer:
            for s_q in SingleChoiceQuestions:
                if key == s_q[0]:  # 题目核对
                    if single_answer[key].split('.')[0] == s_q[2]:  # 答案校对
                        single_score += 5
                    else:
                        check_wrong_answer.append([key, s_q[2]])
                        for s in s_q[6]:
                            # for path in s.split('|'):
                            #     wrong_knowledge_name.append(path)
                            wrong_knowledge_name.append(s.split('|')[-1])
                        for Id in s_q[7]:
                            wrong_knowledge_id.append(Id)
                        wrong_single_num += 1

        print('单选题得分：', single_score)
        # 判断题得分
        tf_score = 0
        # 判断题错题数
        wrong_tf_num = 0
        for key in tf_answer:
            for tf_q in TureFalseQuestions:
                if key == tf_q[0]:  # 题目核对
                    if tf_answer[key] == tf_q[2]:  # 答案校对
                        tf_score += 4
                    else:
                        check_wrong_answer.append([key, tf_q[2]])
                        for tf in tf_q[6]:
                            # for path in tf.split('|'):
                            #     wrong_knowledge_name.append(path)
                            wrong_knowledge_name.append(tf.split('|')[-1])
                        for Id in tf_q[7]:
                            wrong_knowledge_id.append(Id)
                        wrong_tf_num += 1
        print('判断题得分：', tf_score)
        # 多选题得分
        mul_score = 0
        # 多选题错题数
        wrong_mul_num = 0
        for key in mul_answer:
            for m_q in MultipleChoiceQuestions:
                if key == m_q[0]:  # 题目核对
                    if [i.split('.')[0] for i in mul_answer[key]] == m_q[2]:  # 答案校对
                        mul_score += 6
                    else:
                        check_wrong_answer.append([key, m_q[2]])
                        for m in m_q[6]:
                            # for path in m.split('|'):
                            #     wrong_knowledge_name.append(path)  # 储存整条知识点路径
                            wrong_knowledge_name.append(m.split('|')[-1])  # 只储存单个知识点
                        for Id in m_q[7]:
                            wrong_knowledge_id.append(Id)
                        wrong_mul_num += 1
        print('多选题得分：', mul_score)
        total_score = single_score + tf_score + mul_score
        # 错误知识点汇总
        # 错误知识点统计推荐  eg:[['ICN2-1-3', 4], ['IC4-3-5', 4], ['ICN3-1-3', 3]]
        wrong_knowledge_recommend_num = {}

        print(wrong_knowledge_id)
        print(wrong_knowledge_name)
        print(len(wrong_knowledge_name))
        print(len(wrong_knowledge_id))

        for key in wrong_knowledge_id:
            wrong_knowledge_recommend_num[key] = wrong_knowledge_recommend_num.get(key, 0) + 1
        wrong_knowledge_recommend_num = sorted(wrong_knowledge_recommend_num.items(), key=lambda x: x[1], reverse=True)
        wrong_knowledge_recommend_num = [list(num) for num in wrong_knowledge_recommend_num]
        print('知识点推荐模型输入：', wrong_knowledge_recommend_num)

        Summary_wrong_knowledge_points = '|'.join(str(i) for i in wrong_knowledge_id)
        print('错误知识点汇总：', Summary_wrong_knowledge_points)
        print('错误题目汇总：', check_wrong_answer)

        print('总分：', total_score)
        models.UserHistoryBehavior.objects.create(username=request.user.username, answer_time=answer_time,
                                                  wrong_single_num=wrong_single_num, single_score=single_score,
                                                  wrong_tf_num=wrong_tf_num, tf_score=tf_score,
                                                  wrong_mul_num=wrong_mul_num, mul_score=mul_score,
                                                  wrong_num=wrong_single_num + wrong_tf_num + wrong_mul_num,
                                                  score=total_score,
                                                  wrong_knowledge_points=Summary_wrong_knowledge_points)

        # 统计知识点错误次数 eg:[['文化价值观', 15], ['国际贸易实务', 8], ['日本文化', 7], ['英国文化', 6], ['沟通风格', 5], ['非言语交际', 4]]
        wrong_knowledge_num = {}
        for key in wrong_knowledge_name:
            wrong_knowledge_num[key] = wrong_knowledge_num.get(key, 0) + 1
        wrong_knowledge_num = sorted(wrong_knowledge_num.items(), key=lambda x: x[1], reverse=True)
        wrong_knowledge_num = [list(num) for num in wrong_knowledge_num]
        print(wrong_knowledge_num[:6])
        # for wrong_knowledge, wrong_knowledge_recommend_id in zip(wrong_knowledge_num, wrong_knowledge_recommend_num):
        #     # 储存用户错误知识点次数
        #     if models.WrongKnowledgeNum.objects.filter(knowledgeName=wrong_knowledge[0],
        #                                                knowledgeID=wrong_knowledge_recommend_id[0],
        #                                                username=request.user.username):
        #         WrongNum = models.WrongKnowledgeNum.objects.filter(knowledgeName=wrong_knowledge[0],
        #                                                            knowledgeID=wrong_knowledge_recommend_id[0],
        #                                                            username=request.user.username)[0].WrongNum
        #         WrongNum += wrong_knowledge[1]
        #         models.WrongKnowledgeNum.objects.filter(knowledgeName=wrong_knowledge[0],
        #                                                 knowledgeID=wrong_knowledge_recommend_id[0],
        #                                                 username=request.user.username).update(WrongNum=WrongNum)
        #     else:
        #         models.WrongKnowledgeNum.objects.create(knowledgeName=wrong_knowledge[0],
        #                                                 knowledgeID=wrong_knowledge_recommend_id[0],
        #                                                 WrongNum=wrong_knowledge[1], username=request.user.username)

        return JsonResponse({'score': total_score, 'wrong_knowledge_num': wrong_knowledge_num[:6],
                             'check_wrong_answer': check_wrong_answer,
                             'wrong_knowledge_recommend_num': wrong_knowledge_recommend_num}, safe=False)
    else:
        data_path = os.path.dirname(os.path.dirname(__file__))
        SingleChoiceQuestions, MultipleChoiceQuestions, TureFalseQuestions = csv2list.getExam(data_path)
        # 保证每次做题的题目都不完全相同
        return render(request, 'examination.html',
                      {'SingleChoiceQuestions': random.sample(list(SingleChoiceQuestions), 10),
                       'MultipleChoiceQuestions': random.sample(list(MultipleChoiceQuestions), 5),
                       'TureFalseQuestions': random.sample(list(TureFalseQuestions), 5)})


# 用户行为分析
@login_required
def userAnalysis(request):
    if request.method == 'POST':
        UserBehaviors = models.UserHistoryBehavior.objects.filter(username=request.user.username)
        history = []
        answer_time = ['答题时间']
        single_score = ['单选题得分']
        tf_score = ['判断题得分']
        mul_score = ['多选题得分']
        if UserBehaviors:
            for userBehavior in UserBehaviors:
                answer_time.append(str(userBehavior.answer_time))
                single_score.append(userBehavior.single_score)
                tf_score.append(userBehavior.tf_score)
                mul_score.append(userBehavior.mul_score)
                # print('用户：', userBehavior.username)
                # print('答题时间：', userBehavior.answer_time)
                # print('得分：', userBehavior.score)
                # print('薄弱知识点：', userBehavior.wrong_knowledge_points)
            history.append(answer_time)
            history.append(single_score)
            history.append(tf_score)
            history.append(mul_score)
            # print(history)
            return JsonResponse({'status': 'success', 'history': history}, safe=False)
        else:
            history.append(answer_time)
            history.append(single_score)
            history.append(tf_score)
            history.append(mul_score)
            return JsonResponse({'status': 'fail', 'history': history}, safe=False)
    else:
        return render(request, 'userAnalysis.html')


# 知识点推荐页面
@login_required
def recommend(request):
    if request.method == 'POST':
        # wrong_knowledge_recommend_num = [i.knowledgeID for i in
        #                                  models.WrongKnowledgeNum.objects.filter(username=request.user.username)]
        # print(wrong_knowledge_recommend_num)
        # knowledge_points = recommend_nodes.recommend_nodes(wrong_knowledge_recommend_num)
        # data_path = os.path.dirname(os.path.dirname(__file__))
        # print(data_path)
        # SingleChoiceQuestions, MultipleChoiceQuestions, TureFalseQuestions = csv2list.getExam(data_path)
        # oc_q_recommend, mc_q_recommend, tf_q_recommend = list2ques.get_ques_recommend(SingleChoiceQuestions,
        #                                                                               MultipleChoiceQuestions,
        #                                                                               TureFalseQuestions,
        #                                                                               knowledge_points)
        # print(oc_q_recommend, tf_q_recommend, mc_q_recommend)
        # return JsonResponse({'status': 'yes', 'SingleChoiceQuestions': random.sample(list(oc_q_recommend), 4),
        #                      'MultipleChoiceQuestions': random.sample(list(tf_q_recommend), 2),
        #                      'TureFalseQuestions': random.sample(list(mc_q_recommend), 2)}, safe=False)

        return JsonResponse({'status': 'yes'})
    else:
        # data = models.WrongKnowledgeNum.objects.all().values_list('knowledgeName', 'WrongNum')
        # data = models.WrongKnowledgeNum.objects.all().values_list('knowledgeName')
        # print('错误知识点：', [i[0].replace('}', '') for i in data])
        # graph_json = kg_name2json.get_triplet_json([i[0] for i in data])
        return render(request, 'recommend.html')


# 用户选择已掌握知识点
@login_required
def mastered(request):
    if request.method == 'POST':
        data = request.POST.get('answer')
        print(data)
    return JsonResponse({'score': 100}, safe=False)
