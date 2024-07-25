import numpy as np

def edge2mat(link, num_node):
    A = np.zeros((num_node, num_node))
    for i, j in link:
        A[j, i] = 1
    return A

def normalize_digraph(A):
    Dl = np.sum(A, 0)
    h, w = A.shape
    Dn = np.zeros((w, w))
    for i in range(w):
        if Dl[i] > 0:
            Dn[i, i] = Dl[i] ** (-1)
    AD = np.dot(A, Dn)
    return AD

def get_spatial_graph(num_node, hierarchy):
    A = []
    for i in range(len(hierarchy)):
        A.append(normalize_digraph(edge2mat(hierarchy[i], num_node)))

    A = np.stack(A)

    return A

def get_spatial_graph_original(num_node, self_link, inward, outward):
    I = edge2mat(self_link, num_node)
    In = normalize_digraph(edge2mat(inward, num_node))
    Out = normalize_digraph(edge2mat(outward, num_node))
    A = np.stack((I, In, Out))
    return A

def normalize_adjacency_matrix(A):
    node_degrees = A.sum(-1)
    degs_inv_sqrt = np.power(node_degrees, -0.5)
    norm_degs_matrix = np.eye(len(node_degrees)) * degs_inv_sqrt
    return (norm_degs_matrix @ A @ norm_degs_matrix).astype(np.float32)

def get_graph(num_node, edges):

    I = edge2mat(edges[0], num_node)
    Forward = normalize_digraph(edge2mat(edges[1], num_node))
    Reverse = normalize_digraph(edge2mat(edges[2], num_node))
    A = np.stack((I, Forward, Reverse))
    return A # 3, 22, 22

def get_hierarchical_graph(num_node, edges):
    A = []
    for edge in edges:
        A.append(get_graph(num_node, edge))
    A = np.stack(A)
    return A

def get_groups(dataset='Briareo', CoM=0):
    groups  =[]
    
    if dataset == 'Briareo':
        if CoM == 0:
            groups.append([0])
            groups.append([1, 2])
            groups.append([18, 14, 10, 6, 3])
            groups.append([19, 15, 11, 7, 4])
            groups.append([20, 16, 12, 8, 5])
            groups.append([21, 17, 13, 9])

        ## Center of mass : 1
        elif CoM == 1:
            groups.append([1])
            groups.append([0, 6, 10, 14, 18])
            groups.append([2, 7, 11, 15, 19])
            groups.append([3, 8, 12, 16, 20])
            groups.append([4, 9, 13, 17, 21])
            groups.append([5])
        
        ## Center of mass : 9
        elif CoM == 9:
            groups.append([9])
            groups.append([8])
            groups.append([7])
            groups.append([6])
            groups.append([1])
            groups.append([0, 10, 14, 18])
            groups.append([2, 11, 15, 19])
            groups.append([3, 12, 16, 20])
            groups.append([4, 13, 17, 21])
            groups.append([5])   

        else:
            raise ValueError()
        
    return groups

def get_edgeset(dataset='Briareo', CoM=0):
    groups = get_groups(dataset=dataset, CoM=CoM)
    

    identity = []
    forward_hierarchy = []
    reverse_hierarchy = []

    for i in range(len(groups) - 1):
        self_link = groups[i] + groups[i + 1]
        self_link = [(i, i) for i in self_link]
        identity.append(self_link)
        forward_g = []
        for j in groups[i]:
            for k in groups[i + 1]:
                forward_g.append((j, k))
        forward_hierarchy.append(forward_g)
        
        reverse_g = []
        for j in groups[-1 - i]:
            for k in groups[-2 - i]:
                reverse_g.append((j, k))
        reverse_hierarchy.append(reverse_g)

    edges = []
    for i in range(len(groups) - 1):
        edges.append([identity[i], forward_hierarchy[i], reverse_hierarchy[-1 - i]])

    return edges