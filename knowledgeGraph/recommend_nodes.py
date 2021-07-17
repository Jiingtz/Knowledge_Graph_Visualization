from knowledgeGraph.recommendation import *
import networkx as nx
from knowledgeGraph.neo2data import *


def recommend_nodes(node_id_set):
    # node_id_set = [['IC2-1-1', 2], ['IC2-1-2', 2]]
    labels = ['课程', '一级知识点', '二级知识点', '三级知识点']
    labelSet = creatLabelSet(labels)
    nodeSet = getNodeSetByLabelSet(labelSet)
    FromToSet = getFromToSetByLabelSet(labelSet)

    graph = nx.DiGraph()
    graph.add_nodes_from(nodeSet)
    graph.add_edges_from(FromToSet)

    model = N2VModel(graph)
    result_np = model.recommend(node_id_set)
    return result_np[0:10]


