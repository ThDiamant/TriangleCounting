from igraph import *

newDegrees = {}
neighborsMap = {}

def sortNeighbors(neighbors):
    nIndices = []
    nDegrees = []
    for u in neighbors:
        nIndices.append(u.index)
        nDegrees.append(newDegrees[u.index])
    return [x for _, x in sorted(zip(nDegrees, nIndices), reverse=False)]

def getSortedNeighbors(index, graph):
    value = neighborsMap.get(index)
    if value is None:
        node = graph.vs[index]
        neighbors = node.neighbors()
        value = sortNeighbors(neighbors)
        neighborsMap[index] = value
    return value

def compact_fwd(graph, prob_threshold=0):
    vs = VertexSeq(graph)
    degrees = graph.degree()
    indices = vs.indices
    sortedIndices = []
    sort = sorted(zip(degrees, indices), reverse=True)
    for x, y in sort:
        sortedIndices.append(y)
        newDegrees[y] = x
    # skip first node
    for i in range(len(sortedIndices) - 2, -1, -1):
        newDegrees[sortedIndices[i]] = newDegrees[sortedIndices[i + 1]] + 1

    triangle_counter = 0
    for v in sortedIndices:
        vDegree = newDegrees[v]
        vNeighborIndex = 0
        nSortedIndices = getSortedNeighbors(v, graph)
        for u in nSortedIndices:
            uDegree = newDegrees[u]
            if uDegree <= vDegree:
                internalVNeighborIndex = vNeighborIndex
                # ensure that we wont request an invalid index (we have reach the end of the neighbors)
                if len(nSortedIndices) <= internalVNeighborIndex + 1:
                    break
                uNeighborIndex = 0
                uNSortedIndices = getSortedNeighbors(u, graph)
                # ensure that we wont request an invalid index (we have reach the end of the neighbors)
                if len(uNSortedIndices) == 0:
                    break
                first = True
                internalVNeighborIndex += 1
                while True:
                    if first:
                        v1Index = nSortedIndices[internalVNeighborIndex]
                        # Loop until we find a node with valid degree or to check every neighbor
                        while newDegrees[v1Index] < vDegree:
                            internalVNeighborIndex += 1
                            if len(nSortedIndices) <= internalVNeighborIndex:
                                break
                            v1Index = nSortedIndices[internalVNeighborIndex]
                        if len(nSortedIndices) <= internalVNeighborIndex:
                            break
                        u1Index = uNSortedIndices[uNeighborIndex]
                        # Loop until we find a node with valid degree or to check every neighbor
                        # In this case, we should move to the next node of v neighbors as there are no
                        # triangles here or we have already count them
                        while newDegrees[u1Index] < vDegree:
                            uNeighborIndex += 1
                            if len(uNSortedIndices) <= uNeighborIndex + 1:
                                break
                            u1Index = uNSortedIndices[uNeighborIndex]
                        if len(uNSortedIndices) <= uNeighborIndex + 1:
                            break
                        first = False
                    if newDegrees[u1Index] > newDegrees[v1Index]:
                        # ensure that we wont request an invalid index (we have reach the end of the neighbors)
                        if len(nSortedIndices) <= internalVNeighborIndex + 1:
                            break
                        internalVNeighborIndex += 1
                        v1Index = nSortedIndices[internalVNeighborIndex]
                    elif newDegrees[u1Index] < newDegrees[v1Index]:
                        # ensure that we wont request an invalid index (we have reach the end of the neighbors)
                        if len(uNSortedIndices) <= uNeighborIndex + 1:
                            break
                        uNeighborIndex += 1
                        u1Index = uNSortedIndices[uNeighborIndex]
                    else:
                        triangle_counter += 1
                        # ensure that we wont request an invalid index (we have reach the end of the neighbors)
                        if len(uNSortedIndices) <= uNeighborIndex + 1:
                            break
                        uNeighborIndex += 1
                        u1Index = uNSortedIndices[uNeighborIndex]
                        # In this case, we should move to the next node of v neighbors as there are no
                        # triangles here or we have already count them
                        if newDegrees[u1Index] >= vDegree:
                            # ensure that we wont request an invalid index (we have reach the end of the neighbors)
                            if len(nSortedIndices) <= internalVNeighborIndex + 1:
                                break
                            internalVNeighborIndex += 1
                            v1Index = nSortedIndices[internalVNeighborIndex]
                vNeighborIndex += 1

    if prob_threshold > 0:
        triangle_counter = round(triangle_counter * (1 / pow(prob_threshold, 3)))

    print('CompactForward - Approximate Triangle Count with parameter {}: {}'.format(prob_threshold,
                                                                                     triangle_counter))
    return triangle_counter
