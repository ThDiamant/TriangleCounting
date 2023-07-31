from igraph import *
# import networkx as nx

# IGRAPH
def brute_force(graph, prob_threshold=0):
    """
    Implements the Brute Force algorithm to count the number of triangles in the input graph.
    The algorithm is the following: For every possible triplet, examine if that triplet is a triangle

    Input(s):
        g [igraph.Graph]: Input graph we want to count the number of triangles of.
    Output(s):
        noTriangles [int] Number of triangles in the graph.
    """
    vs = VertexSeq(graph)
    triangle_counter = 0
    for u in range(0, len(vs)):
        for v in range(u + 1, len(vs)):
            for w in range(v + 1, len(vs)):
                if graph.are_connected(u, v) and graph.are_connected(v, w) and graph.are_connected(u, w):
                    triangle_counter += 1

    if prob_threshold > 0:
        triangle_counter = round(triangle_counter * (1 / pow(prob_threshold, 3)))

    print('Brute Force - Approximate Triangle Count with parameter {}: {}'.format(prob_threshold, triangle_counter))

    return triangle_counter


# NETWORKX
'''
def brute_force(graph, delete_proba_threshold=0):

    triangle_counter = 0
    len_nodes = len(list(graph.nodes()))

    for u in range(0, len_nodes):
        for v in range(u + 1, len_nodes):
            for w in range(v + 1, len_nodes):
                if v in graph[u] and v in graph[w] and u in graph[w]:
                    triangle_counter += 1
    
    if delete_proba_threshold > 0:
        triangle_counter = round(triangle_counter * (1 / pow(delete_proba_threshold, 3)))

    return triangle_counter
'''

