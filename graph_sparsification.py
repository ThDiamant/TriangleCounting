from igraph import *
import random
import pandas as pd

# IGRAPH
def doulion(full_graph, insert_probability_threshold):
    edges_ids_to_inserted = [(e.source, e.target) for e in full_graph.es if random.random() < insert_probability_threshold]
    new_edges = pd.DataFrame(edges_ids_to_inserted, columns =['Source', 'Target'])
    g_sparse = Graph.DataFrame(new_edges, directed=False)
    print("Graph for param {} has {} nodes and {} edges".format(insert_probability_threshold , len(g_sparse.vs()), len(g_sparse.es())))
    return g_sparse, insert_probability_threshold

# NETWORKX
'''
def doulion(full_graph, delete_proba_threshold):
    g_sparse = full_graph.copy()
    for source, target in g_sparse.edges():
        if random.random() > delete_proba_threshold:
            g_sparse.remove_edge(source, target)
    return g_sparse, delete_proba_threshold
'''