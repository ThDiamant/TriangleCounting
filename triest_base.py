import random

reservoir = []

adjecency = {}
triangle_count = 0


def triest_base(edges_file, M, sep):
    global reservoir
    global adjecency
    global triangle_count

    adjecency.clear()
    reservoir.clear()
    triangle_count = 0

    with open(edges_file) as f:
        edges = f.readlines()

    t = 0
    for edge in edges:
        t += 1
        tuple_edge = tuple(map(int, edge.split(sep)))
        u = tuple_edge[0]
        v = tuple_edge[1]
        if u not in adjecency:
            adjecency[u] = []
        if v not in adjecency:
            adjecency[v] = []
        if sample_edge(tuple_edge, t, M):
            reservoir.append(tuple_edge)
            adjecency[u].append(v)
            adjecency[v].append(u)
            update_counters('+', tuple_edge)

    return triangle_count
    

def sample_edge(edge, t, M):
    global reservoir
    global adjecency
    if t <= M:
        return True
    elif flip_biased_coin(M/t):
        edge_to_drop_idx = random.randint(0, M-1)
        u, v = reservoir[edge_to_drop_idx][0], reservoir[edge_to_drop_idx][1]
        adjecency[u].remove(v)
        adjecency[v].remove(u)
        del reservoir[edge_to_drop_idx]
        update_counters('-', edge)
        return True
    else:
        return False


def update_counters(operation, edge):
    global triangle_count
    intersection = list(set(adjecency[edge[0]]) & set(adjecency[edge[1]]))
    if operation == '+':
        for _ in intersection:
            triangle_count += 1
    else:
        for _ in intersection:
            triangle_count -= 1


def flip_biased_coin(p):
    return True if random.random() < p else False


