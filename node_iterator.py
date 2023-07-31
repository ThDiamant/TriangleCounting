# import networkx as nx
from itertools import combinations
from igraph import *

# IGRAPH
def node_iterator(graph, prob_threshold=0):
    """
    Implements the NodeIterator algorithm to count the number of triangles in the input graph.
    The algorithm is the following: for each vertex u in the graph, for each pair of nodes (v, w) in the neighborhood
    of u, if the edge v-w exists, then a triangle has been found.

    Input(s):
        g [igraph.Graph]: Input graph we want to count the number of triangles of.
    Output(s):
        noTriangles [int] Number of triangles in the graph.
    """
    triangle_counter = 0
    for u in graph.vs():
        # Get neighbours of u
        uNeigh = graph.neighbors(u.index)
        # Create all pairs of size 2
        uNeighPairs = list(combinations(uNeigh, 2))

        for (v, w) in uNeighPairs:
            # Get index of edge between v and w; if it doesn't exist returns -1
            vwEdge = graph.get_eid(v, w, directed=False, error=False)
            # If edge exists
            if vwEdge != -1:
                triangle_counter += 1

    if prob_threshold > 0:
        triangle_counter = round(triangle_counter * (1 / pow(prob_threshold, 3)))

    print('NodeIterator - Approximate Triangle Count with parameter {}: {}'.format(prob_threshold,
                                                                                     triangle_counter // 3))
    return triangle_counter // 3

# NETWORKX
'''
def nodes_connected(g, u, v):
    # Returns True if u and v are connected, False otherwise.
    return u in g.neighbors(v)

def node_iterator(graph, delete_proba_threshold=0):
    """
    Implements the NodeIterator algorithm to count the number of triangles in the input graph.
    The algorithm is the following: for each vertex u in the graph, for each pair of nodes (v, w) in the neighborhood
    of u, if the edge v-w exists, then a triangle has been found.

    Input(s):
        g [networkx.Graph]: Input graph we want to count the number of triangles of.
    Output(s):
        noTriangles [int] Number of triangles in the graph.
    """
    # start_time = time.time()
    # tracemalloc.start()
    triangle_counter = 0
    for u in list(graph.nodes):
        # Get neighbours of u
        uNeigh = graph.neighbors(u)
        # Create all pairs of size 2
        uNeighPairs = list(combinations(uNeigh, 2))

        for (v, w) in uNeighPairs:
            if nodes_connected(graph, v, w):
                triangle_counter += 1

    if delete_proba_threshold > 0:
        triangle_counter = round(triangle_counter * (1 / pow(delete_proba_threshold, 3)))\

    # print("--- Node Iterator completed in {:.2f} seconds ---".format(time.time() - start_time))
    # print("--- Node Iterator used {}B of memory ---".format(size(tracemalloc.get_tracemalloc_memory())))
    # tracemalloc.stop()
    return triangle_counter // 3
'''


