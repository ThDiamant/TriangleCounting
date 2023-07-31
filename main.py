import igraph as ig
from graph_sparsification import doulion
from brute_force import brute_force
from node_iterator import node_iterator
from compact_fwd import compact_fwd
from triest_base import triest_base
import tracemalloc
from hurry.filesize import size
import time
import sys

# graph_edges_file = 'soc-Slashdot0811.txt' # medium graph https://networkrepository.com/soc-Slashdot0811.php?fbclid=IwAR0dx7noYw-xbuC2gH0bLZ1h_b8Pgzbu36i5mvUEe7CY0xt77vPtVN6rYxo
# graph_edges_file = 'as-skitter-Correct.txt' # Large graph https://snap.stanford.edu/data/as-Skitter.html
graph_edges_file = r"input_graphs/" + 'roadNet-TX-2.txt' # sparse graph https://snap.stanford.edu/data/roadNet-TX.html

# graph_edges_file = r"input_graphs/" + 'facebook_combined.txt'  # test graph

currentGraph = graph_edges_file.split(".")[0].split('/')[-1].strip()
print("---------------------------- Graph: {} ----------------------------".format(currentGraph))

g = ig.Graph.Read_Ncol(graph_edges_file, directed=False)
n, m = len(g.vs()), len(g.es())
print("Full graph has {} nodes and {} edges.".format(n, m))

start_time = time.time()
node_iterator_exact_triangles = node_iterator(g)
print("Node Iterator: %s sec" % (time.time() - start_time))

start_time = time.time()
compact_fwd_exact_triangles = compact_fwd(g)
print("Compact Forward: %s sec" % (time.time() - start_time))

start_time = time.time()
brute_force_exact_triangles = brute_force(g)
print("Brute Force: %s sec" % (time.time() - start_time))

for param in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9):
    print("Start Brute Force with {} param".format(param))
    start_time = time.time()
    doul = doulion(g, param)
    print("Doulion Calculation: %s sec" % (time.time() - start_time))

    start_time = time.time()
    node_iterator_approx_triangles = node_iterator(doul)
    print("Node Iterator: %s sec" % (time.time() - start_time))

    start_time = time.time()
    compact_fwd_approx_triangles = compact_fwd(doul)
    print("Compact Forward: %s sec" % (time.time() - start_time))

    start_time = time.time()
    brute_force_approx_triangles = brute_force(doul)
    print("Brute Force: %s sec" % (time.time() - start_time))

# Change stdout so that everything is written to outFile
orig_stdout = sys.stdout
outFile = r'output_logs/Triest-{}.txt'.format(currentGraph)
f = open(outFile, 'w')
sys.stdout = f

# Triest-Base parameter runs
sep = "\t"
for multiplier in (0.2, 0.4, 0.6, 0.8, 1.0):

    M = int(multiplier*m)
    start_time = time.time()
    tracemalloc.start()
    triest_base_approx_triangles = triest_base(graph_edges_file, M, sep)
    print("Triest Base - Reservoir Size M: {} ({}% of total)".format(M, multiplier*100))
    print('Triest Base - Approximate Triangle Count: {}'.format(triest_base_approx_triangles))
    print("Triest Base: {:.3} sec".format(time.time() - start_time))
    print('Triest Base: {}B of memory'.format(size(tracemalloc.get_tracemalloc_memory())))
    tracemalloc.stop()
    print("-"*100)




