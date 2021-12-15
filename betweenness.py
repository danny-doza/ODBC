import numpy as np
import math

# First two functions were taken from https://networkx.github.io/documentation/networkx-0.37/networkx.centrality-pysrc.html#betweenness_centrality_source
# Changes made by me in said functions have been commented using multi line comments for clarity

def betweenness_centrality_source(G, test_type="dist", pop_weights=None, normalized=True, weighted_edges=False,
                                  sources=None):
    """
    Enchanced version of the method in centrality module that allows
    specifying a list of sources (subgraph).

    weighted_edges:: consider edge weights by running Dijkstra's algorithm          (no effect on unweighted graphs).

    sources:: list of nodes to consider as subgraph

    See Sec. 4 in
    Ulrik Brandes,
    A Faster Algorithm for Betweenness Centrality.
    Journal of Mathematical Sociology 25(2):163-177, 2001.
    http://www.inf.uni-konstanz.de/algo/publications/b-fabc-01.pdf


    This algorithm does not count the endpoints, i.e.
    a path from s to t does not contribute to the betweenness of s and t.
    """
    import heapq

    if sources == None:
        sources = G.nodes()

    ''' test_num is used to identify which test is being performed '''
    # "dist" signifies the distance weighted ODBC test
    # "pop" signifies the population weighted ODBC tests (plural)
    # "dist&pop" signifies the combined distance and population weighted ODBC TEST <<<<<<<< NEEEDS WOORK!!!! (never used)

    ''' call my own functions here '''
    node_weights = {}
    nodes = list(G.nodes())

    if test_type == "dist":
        # distances only calculated for use in weights calculations
        distances = calc_distances_helper(G, sources, weighted_edges)
        for source in sources:
            for node in nodes:
                if node not in distances[source]:
                    distances[source][node] = 0
        # weights used to give importance to nodes in shortest paths based on nearest source
        weights = calc_weights_helper(G, sources, distances)
        node_weights = weights.copy()

        # print(node_weights)
        # print("MY DISTANCES:", distances)

    elif test_type == "pop":
        if pop_weights is None:
            print("pop_weights is empty while performing pop test. Proceeding with all node vals set to 1.")
            for val in nodes:
                node_weights[val] = 1
        else:
            node_weights = pop_weights.copy()

        for node in nodes:
            if node not in node_weights:
                node_weights[node] = 0
        #print("POP NODE WEIGHTS:", node_weights)
        sorted_node_weights = np.sort(list(node_weights.values()))
        Q1 = np.percentile(sorted_node_weights, 25, interpolation='midpoint')
        Q3 = np.percentile(sorted_node_weights, 75, interpolation='midpoint')
        IQR = Q3 - Q1
        highest_pop = Q3 + 1.5 * IQR
        lowest_pop = Q1 - 1.5 * IQR
        adjusted_node_weights = {}
        for node in nodes:
            if node_weights[node] > highest_pop:
                adjusted_node_weights[node] = highest_pop
            elif node_weights[node] < lowest_pop:
                adjusted_node_weights[node] = lowest_pop
            else:
                adjusted_node_weights[node] = node_weights[node]
        node_weights = adjusted_node_weights.copy()

        highest_pop = max(list(node_weights.values()))
        lowest_pop = min(list(node_weights.values()))

        #print(Q1, Q3, IQR, highest_pop, lowest_pop)

        for node in nodes:
            node_weights[node] = 0.0 + ((node_weights[node] - lowest_pop) * 1.0) / (highest_pop - lowest_pop)
        #print(node_weights)

    else:
        print("Error: Please enter defined value for test_type")
        return None

    betweenness = dict.fromkeys(G, 0.0)
    for s in sources:
        ''' added weights, v_weights vars to function call '''
        S, P, D, sigma = _brandes_betweenness_helper(G, s, weighted_edges)

        if test_type == "pop":
            new_node_weights = calc_pop_weights_from_pops(nodes, node_weights, P)

        delta = dict.fromkeys(G, 0)  # unnormalized betweenness
        while S:
            w = S.pop()
            for v in P[w]:
                ''' added weights are accounted for here '''
                if v != s:
                    if test_type == "dist":
                        delta[v] = delta[v] + (float(sigma[v]) / float(sigma[w])) * (1.0 + delta[w]) * node_weights[s][v]
                    elif test_type == "pop":
                        delta[v] = delta[v] + (float(sigma[v]) / float(sigma[w])) * (1.0 + delta[w]) * new_node_weights[v]
                    #elif test_type == "dist&pop":
                    #    delta[v] = delta[v] + (float(sigma[v]) / float(sigma[w])) * (1.0 + delta[w]) * (
                    #                (new_node_weights[v] * dist_weights[v][s]) / node_weights[w])
                    else:
                        delta[v] = delta[v] + (float(sigma[v]) / float(sigma[w])) * (1.0 + delta[w]) * node_weights[v]

            if w == s:
                continue
            betweenness[w] = betweenness[w] + delta[w]

    # normalize to size of entire graph
    if normalized and G.number_of_edges() > 1:
        order = len(betweenness)
        scale = 1.0 / ((order - 1) * (order - 2))
        for v in betweenness:
            betweenness[v] *= scale

    return betweenness


def _brandes_betweenness_helper(G, root, weighted_edges):
    """
    Helper for betweenness centrality and edge betweenness centrality.

    Runs single-source shortest path from root node.

    weighted_edges:: consider edge weights

    Finds::

    S=[] list of nodes reached during traversal
    P={} predecessors, keyed by child node
    D={} distances
    sigma={} indexed by node, is the number of paths to root
    going through the node
    """
    import heapq
    S = []
    P = {}
    for v in G:
        P[v] = []
    sigma = dict.fromkeys(G, 0.0)
    D = {}
    sigma[root] = 1

    if not weighted_edges:  # use BFS
        D[root] = 0
        Q = [root]
        while Q:  # use BFS to find shortest paths
            v = Q.pop(0)
            S.append(v)
            for w in G.neighbors(v):  # for w in G.adj[v]: # speed hack, exposes internals
                if w not in D:
                    Q.append(w)
                    D[w] = D[v] + 1
                if D[w] == D[v] + 1:  # this is a shortest path, count paths
                    sigma[w] = sigma[w] + sigma[v]
                    P[w].append(v)  # predecessors
    else:  # use Dijkstra's algorithm for shortest paths,
        # modified from Eppstein
        push = heapq.heappush
        pop = heapq.heappop
        seen = {root: 0}
        Q = []  # use Q as heap with (distance,node id) tuples
        push(Q, (0, root, root))
        while Q:
            (dist, pred, v) = pop(Q)
            if v in D:
                continue  # already searched this node.
            sigma[v] = sigma[v] + sigma[pred]  # count paths
            S.append(v)
            D[v] = seen[v]
            for w in G.neighbors(v):  # for w in G.adj[v]: # speed hack, exposes internals
                vw_dist = D[v] + G.get_edge_data(v, w)['weight']
                if w not in D and (w not in seen or vw_dist < seen[w]):
                    seen[w] = vw_dist
                    push(Q, (vw_dist, v, w))
                    P[w] = [v]
                elif vw_dist == seen[w]:  # handle equal paths
                    sigma[w] = sigma[w] + sigma[v]
                    P[w].append(v)
    return S, P, D, sigma


def calc_pop_weights_from_pops(nodes, node_weights, P):
    new_node_weights = {}
    for node in nodes:
        curr_node = node

        # weight that will be assigned to node after summing pops across shortest dist.
        single_node_weight = 0
        nodes_in_path_count = 0
        while P[curr_node] != []:
            # add node_weights val (pop. val for node) of the previous node to single_node_weight
            # (min() used simply to make a choice between multiple shortest path options)
            single_node_weight += node_weights[min(P[curr_node])]
            # add 1 to nodes_in_path_count
            nodes_in_path_count += 1
            # select a new node through which to arrive to source and form a full path
            curr_node = min(P[curr_node])

        # if there is a path between source and dest.
        if nodes_in_path_count != 0:
            # calc. average
            single_node_weight = single_node_weight / nodes_in_path_count
        else:
            single_node_weight = 1

        # add calculated val. to new weights dict.
        new_node_weights[node] = single_node_weight

    # print("NEW POP NODE WEIGHTS:", new_node_weights)
    return new_node_weights


def calc_distances_helper(G, sources, weighted_edges):
    all_distances = {}
    for s in sources:
        import heapq
        D = {}
        if not weighted_edges:  # BFS for unweighted graphs
            D[s] = 0
            Q = [s]
            while Q:  # use BFS to find shortest paths
                v = Q.pop(0)
                for w in G.neighbors(v):
                    if w not in D:
                        Q.append(w)
                        D[w] = D[v] + 1
            all_distances[s] = D
        else:
            root = s
            push = heapq.heappush
            pop = heapq.heappop
            seen = {root: 0}
            Q = []
            push(Q, (0, root, root))
            while Q:
                (dist, pred, v) = pop(Q)
                if v in D:
                    continue
                D[v] = seen[v]
                for w in G.neighbors(v):
                    vw_dist = D[v] + G.get_edge_data(v, w)['weight']
                    if w not in D and (w not in seen or vw_dist < seen[w]):
                        seen[w] = vw_dist
                        push(Q, (vw_dist, v, w))
            all_distances[s] = D
    return all_distances


def calc_weights_helper(G, sources, distances):
    nodes = list(G.nodes())

    min_dist_to_source_per_node = {}
    for n in nodes:
        min_dist = math.inf
        for s in sources:
            if s != n:
                curr_dist = distances[s][n]

                if curr_dist != 0 and curr_dist < min_dist:
                    min_dist = curr_dist
            else:
                min_dist_to_source_per_node[n] = 0.00001

        min_dist_to_source_per_node[n] = min_dist

    # print("MIN_DIST_TO_SOURCE_PER_NODE:", min_dist_to_source_per_node)

    all_denominators = {}
    for s in sources:
        all_denominators[s] = {}
        for n in nodes:
            if n not in all_denominators[s]:
                all_denominators[s][n] = 0
            if s != n and distances[s][n] != 0:
                all_denominators[s][n] += min_dist_to_source_per_node[n] / distances[s][n]
            else:
                all_denominators[s][n] = math.inf

        if all_denominators[s][n] == 0:
            all_denominators[s][n] = 1

    # print("ALL DENOMINATORS:", all_denominators)

    all_weights = {}
    for s in sources:
        all_weights[s] = {}
        for n in nodes:
            min_dist_to_source = min_dist_to_source_per_node[n]
            if s != n and distances[s][n] != 0:
                ''' unnormalized weights'''
                all_weights[s][n] = min_dist_to_source / distances[s][n]
                ''' normalized weights '''
                # all_weights[s][n] = (min_dist/distances[s][n])/all_denominators[s][n]
            else:
                all_weights[s][n] = 1

            # print("Hospital", s, "given weight of", s_weights.get(n))
            # print("Dict. of weights for", n, ":", all_weights[n])

    # print("ALL WEIGHTS:", all_weights)
    return all_weights
