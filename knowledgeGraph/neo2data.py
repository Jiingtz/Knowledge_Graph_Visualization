# -*- encoding: utf-8 -*-
# @Time : 2021/7/2 10:46
# @Author : midww
# @File : neo2data.py


from py2neo import Graph


graph = Graph("http://localhost:7474", auth=("neo4j", "ztj19991124"))


def creatLabelSet(Labels):
    labelSet = []
    for label in Labels:
        labelSet.append([label])
    return labelSet


def nodes2Set(nodes):
    nodeSet = []
    for node in nodes:
        nodeSet.append(node.get('n')['knowledgeId'])
    return nodeSet


def getAllNodeSet():
    nodes = graph.run('MATCH (n) RETURN n')
    nodeSet = nodes2Set(nodes)
    return nodeSet


def getNodeSetByLabelSet(labelSet):
    nodes = graph.run('MATCH (n) where labels(n) in {} RETURN n'
                      .format(labelSet))
    nodeSet = nodes2Set(nodes)
    return nodeSet


def FromTos2Set(FromTos):
    FromToSet = []
    for FromTo in FromTos:
        FromToSet.append([FromTo.get('n')['knowledgeId'],
                          FromTo.get('m')['knowledgeId']])
    return FromToSet


def getAllFromToSet():
    FromTos = graph.run('MATCH (n)-[]->(m) return n, m')
    FromToSet = FromTos2Set(FromTos)
    return FromToSet


def getFromToSetByLabelSet(labelSet):
    FromTos = graph.run('MATCH (n)-[]->(m) WHERE labels(n) in {} and labels(m) in {} return n,m'
                        .format(labelSet, labelSet))
    FromToSet = FromTos2Set(FromTos)
    return FromToSet

