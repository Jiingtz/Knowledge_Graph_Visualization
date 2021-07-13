# _*_ coding: utf-8 _*_ 
""" 
@Time    : 2021/6/26 22:36  
@Author  : Du QiYong  
@Version : V 1.0 
@File    : createGraph.py
@desc    : 处理 XLore_Apis返回的json数据 
"""
import time
from knowledgeGraph import XLore_Apis as XA
import json
from py2neo import Graph
from knowledgeGraph import baike

g = Graph("http://localhost:7474", auth=("neo4j", "ztj19991124"))
label_name = ['课程', '一级知识点', '二级知识点', '三级知识点', '子知识点']

mc = baike.MainCrawler()


def get_label_Hyponymy(str):
    json_str = XA.get_word(str)  # 调用API 
    data = json.loads(json_str)  # 解析json 
    hyponymy = []
    last_tag = False
    if 'Classes' not in data:
        return hyponymy, last_tag
    if len(data['Classes']) == 0:
        return hyponymy, last_tag
    items = data['Classes'][0]['Hyponymy']
    if len(items) == 0:
        last_tag = True
        items = data['Classes'][0]['Instances']
    for item in items:
        hyponymy.append(item['Label'])
    return hyponymy, last_tag


def create_node_rel(node1_name, node2_name, node1_type, node2_type):
    cypher = "merge (n1:`" + node1_type + "` {name:'" + node1_name + "'}) merge (n2:`" + \
             node2_type + "` {name:'" + node2_name + "'})"
    g.run(cypher)
    cypher = "match (n1:`" + node1_type + "` {name:'" + node1_name + "'}) merge (n2:`" + \
             node2_type + "` {name:'" + node2_name + "'}) merge (n1)-["":Subordinate]->(n2)"
    g.run(cypher)


def data2neo(label, count, choice, max_count=5):
    if (count + 2) > max_count:
        return
    if choice == 'xlore':
        items, tag = get_label_Hyponymy(label)
    else:
        items, tag = baike.getBaiKe(label, mc)
    if tag:
        print('未获取到数据')
        return
    print(label, items)
    count1 = count
    count2 = count + 1
    if count > 3:
        count1 = 4
        count2 = 4
    label1_type = label_name[count1]
    label2_type = label_name[count2]
    for item in items:
        create_node_rel(label, item, label1_type, label2_type)
        data2neo(item, count + 1, choice, max_count)


def structure(label, choice, max_count=5):
    time_start = time.time()
    status = 'NO'
    cypher = "match (n:`课程` {name:'" + label + "'}) return n"
    if any(g.run(cypher)):
        print('该课程的知识图谱已经存在。')
        return status
    count = 0
    cypher = "merge (n:`课程`{name:'" + label + "'})"
    g.run(cypher)
    data2neo(label, count, choice, max_count)
    status = 'YES'
    time_end = time.time()
    print('totally cost', time_end - time_start)
    return status

# structure('软件工程', choice=1, max_count=4)
# print(get_label_Hyponymy('软件工程'))
