# -*- encoding: utf-8 -*-
# @Time : 2021/7/2 16:03
# @Author : midww
# @File : recommendation.py


from node2vec import Node2Vec
import numpy as np


class N2VModel:
    def __init__(self, graph=None,
                 dimensions=50,
                 walk_length=40,
                 num_walks=100,
                 workers=4,
                 p: float = 0.5,
                 q: float = 1.5):
        node2vec = Node2Vec(graph,
                            dimensions=dimensions,
                            walk_length=walk_length,
                            num_walks=num_walks,
                            workers=workers,
                            p=p,
                            q=q)
        self.model = node2vec.fit(window=10)

    def recommend(self, node_id_set):
        final_result = []
        for node_id in node_id_set:
            results_0 = self.model.wv.most_similar(node_id[0])
            results_1 = []
            for result_0 in results_0:
                score = result_0[1] * node_id[1] * 0.5
                result_1 = [result_0[0], score]
                results_1.append(result_1)
            if final_result is None:
                final_result += results_1
            else:
                f_r_nodes_name = [i[0] for i in final_result]
                for node in results_1:
                    if node[0] in f_r_nodes_name:
                        final_result[f_r_nodes_name.index(node[0])][1] += node[1]
                    else:
                        final_result.append(node)

        f_r_nodes_name = [i[0] for i in final_result]
        for node in node_id_set:
            if node[0] in f_r_nodes_name:
                final_result[f_r_nodes_name.index(node[0])][1] += node[1] * 0.7
            else:
                final_result.append(node)
        np_result = np.array(final_result)
        np_result = np_result[np.lexsort(np_result.T)]
        np_result = np_result[::-1]
        return np_result









