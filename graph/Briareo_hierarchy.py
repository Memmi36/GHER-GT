from audioop import reverse
import sys
import numpy as np

sys.path.extend(['../'])
from graph import tools

num_node = 22

class Graph:
    def __init__(self, CoM=0, labeling_mode='spatial'):
        self.num_node = num_node
        self.CoM = CoM
        self.A = self.get_adjacency_matrix(labeling_mode)
        

    def get_adjacency_matrix(self, labeling_mode=None):
        if labeling_mode is None:
            return self.A
        if labeling_mode == 'spatial':
            A = tools.get_hierarchical_graph(num_node, tools.get_edgeset(dataset='Briareo', CoM=self.CoM)) # L, 3, 22, 22
        else:
            raise ValueError()
        return A, self.CoM


if __name__ == '__main__':
    g = Graph().A