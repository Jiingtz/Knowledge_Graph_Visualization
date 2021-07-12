# -*- encoding: utf-8 -*-
# @Time : 2021/7/12 14:57
# @Author : midww
# @File : csv2list.py


def getExam(data_path):
    import pandas as pd
    import numpy as np
    import os
    one_choice_pd = pd.read_csv(os.path.join(data_path, 'static/data/one_choice.csv'))
    multi_choice_pd = pd.read_csv(os.path.join(data_path, 'static/data/multi_choice.csv'))
    ture_false_pd = pd.read_csv(os.path.join(data_path, 'static/data/ture_false.csv'))

    single_choice_questions = np.array(one_choice_pd)
    multi_choice_questions = np.array(multi_choice_pd)
    ture_false_questions = np.array(ture_false_pd)

    for question in single_choice_questions:
        question[0] = question[0].replace('，', ',')
        question[1] = question[1].split('|')
        question[3] = question[3].replace('，', ',')
        question[6] = question[6].split('，')

    for question in multi_choice_questions:
        question[0] = question[0].replace('，', ',')
        question[1] = question[1].split('|')
        question[2] = question[2].split('|')
        question[3] = question[3].replace('，', ',')
        question[6] = question[6].split('，')

    for question in ture_false_questions:
        question[0] = question[0].replace('，', ',')
        question[1] = question[1].split('|')
        if question[2] == 1:
            question[2] = 'Ture'
        else:
            question[2] = 'False'
        question[6] = question[6].split('，')
    return single_choice_questions, multi_choice_questions, ture_false_questions


