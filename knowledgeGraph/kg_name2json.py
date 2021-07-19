# -*- encoding: utf-8 -*-
# @Time : 2021/7/18 8:23
# @Author : midww
# @File : kg_name2json.py
import json

from py2neo import Graph


def get_triplet_json(node_name_set):
    graph = Graph('http://localhost:7474', auth=('neo4j', 'ztj19991124'))
    result = graph.run("with {} as kg_name "
                       "with kg_name match (n) where n.name in kg_name "
                       "with collect (n) as nodes "
                       "unwind nodes as source "
                       "unwind nodes as target "
                       "with source,target where id(source) > id(target) "
                       "with source,target match p=shortestpath((source)-[*]-(target)) "
                       "return p".format(node_name_set))

    paths = result.data()
    triplet = []
    for path in paths:
        for relationship in path.get('p').relationships:
            start_node = relationship.start_node
            source = {'size': int(start_node['size']) * 2,
                      'name': start_node['name'],
                      'id': int(start_node.identity),
                      'label': str(start_node.labels).replace(':', '')}
            end_node = relationship.end_node
            target = {'size': int(end_node['size']) * 0.5,
                      'name': end_node['name'],
                      'id': int(end_node.identity),
                      'label': str(end_node.labels).replace(':', '')}
            rel = {'weight': 5, 'type': type(relationship).__name__}

            triplet.append({'source': source, 'target': target, 'rel': rel})
    return json.dumps(triplet, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    import time

    s = time.time()
    print(get_triplet_json(
        ['文化价值观', '日本文化', '国际贸易实务', '沟通风格', '社会交往与商务礼仪', '商务文化与惯例', '跨文化商务谈判', '备货出货', '非言语交际', '美国文化', '高语境和低语境文化',
         '言语沟通', '社会习俗与礼仪', '会见礼仪', '国际商务谈判', '英国文化', '客户开发', '印度文化', '空间与距离', '非言语沟通', '社会交往通用礼仪', '见面', '不同国家的商务礼仪',
         '亚洲各国商务礼仪', '体态语', '名片交换礼仪']))
    e = time.time()
    print(e - s)
