# -*- encoding: utf-8 -*-
# @Time : 2021/7/15 11:20
# @Author : midww
# @File : list2ques.py

import numpy as np


def choice_ques(questions, rc_nodes):
    question_recommend = []
    score = []
    ques_num = -1
    for oc_q in questions:
        score.append(0)
        ques_num += 1
        for rc_n in rc_nodes:
            if rc_n[0] in oc_q[7]:
                score[ques_num] += float(rc_n[1])
        if score[ques_num] == 0:
            score.pop()
            ques_num -= 1
        else:
            question_recommend.append([oc_q, score[ques_num]])
    if len(question_recommend) != 0:
        question_recommend = np.array(question_recommend)
        index = np.lexsort((question_recommend[:, 1],))
        question_recommend = question_recommend[index]
        question_recommend = question_recommend[::-1]
    return question_recommend


def get_ques_recommend(one_choice_question, multi_choice_question, true_false_question, rc_nodes):
    oc_q_recommend = choice_ques(one_choice_question, rc_nodes)
    mc_q_recommend = choice_ques(multi_choice_question, rc_nodes)
    tf_q_recommend = choice_ques(true_false_question, rc_nodes)
    return oc_q_recommend, mc_q_recommend, tf_q_recommend


