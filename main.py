import networkx

import graph_creation
import TestHandler
import pop_handler
import graph_draw
import calculations
import matplotlib.pyplot as plt


def plot_graph(G, node_sizes, cmap, coords):
    # network drawing
    plt.figure(1, figsize=(50, 50))
    networkx.draw(G, node_size=node_sizes, node_color=cmap, pos=coords)
    plt.show()


def normalize_results(destinations, odbc_values, lower_bound, upper_bound):
    normalized_odbc_values = {}  # dict to be returned

    max_val = float(max(odbc_values.values()))
    min_val = float(min(odbc_values.values()))

    for key, val in odbc_values.items():
        if key in destinations:
            normalized_odbc_values[key] = 1
            continue
        normalized_odbc_values[key] = \
            (upper_bound - lower_bound) * ((val - min_val) / float(max_val - min_val)) + lower_bound
    return normalized_odbc_values


def main():
    # ================================= important variable assignments ============================================== #
    increment = 0.05  # what increment road removal tests should be performed by
    final_removal_amt = 0.1  # final removal amount to be tested
    samples = 125  # num. of samples to perform
    using_lattice = False
    use_weighted_edges = False
    cmap_type = "log"
    # selected removal amount to be tested
    test_type = "pop"  # test type ("simp", "dist", "pop", "dist&pop (NOT FINISHED)")
    test_removal_amt = 0.1
    # =============================================================================================================== #

    # =================================== Graph Creation ============================================================ #
    if using_lattice:
        # --- Lattice Graph Creation
        g_size = 20
        G = networkx.generators.lattice.grid_2d_graph(g_size, g_size)
    else:
        # ---  Kathmandu Graph
        # create adjacency list from 'kathii_wei.txt' file
        kat_dict = graph_creation.create_adjacency_list("kathii_wei.txt")
        # generate graph from adjacency list
        G = networkx.Graph(kat_dict)

    nodes = list(G.nodes())
    # =============================================================================================================== #

    if using_lattice:
        destinations = [(15, 0), (0, 15), (19, 19)]  # dests. for lattice graph

        # - create ( coords ) for plotting later of format dict[node] = [coord x, coord y]
        coords = graph_creation.init_lattice_coords(nodes)

        # --- Define population values manually for test 20 * 20 lattice graph --- #
        pop_values = [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 2, 3, 3, 3, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 2, 3, 4, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 2, 3, 5, 5, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 2, 3, 6, 6, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 2, 3, 6, 6, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 2, 3, 5, 5, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 2, 3, 4, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 2, 3, 3, 3, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 4, 4, 3, 3,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 6, 6, 4, 3, 3,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 6, 6, 4, 3, 3,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 4, 4, 3, 3,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        ]
        # - create ( node_pops_dict ) of format dict[node] = population value
        node_pops_dict = pop_handler.create_lat_node_pop_dict(nodes, pop_values)

        weighted_edges = False
    else:
        destinations = [596, 609, 542]  # destinations for kathmandu network

        # --- Coords creation for network drawing (used later), use filename = r"kathiicoord_original.txt"
        # - ( coords ) of format dict[node] = [coord x, coord y]
        coords = graph_creation.init_coords("kathiicoord_original.txt", nodes)

        # - create ( node_pops_dict ) of format dict[node] = population value
        node_pops_dict = pop_handler.create_kat_node_pop_dict(nodes)

        if use_weighted_edges:
            weighted_edges = calculations.calc_edge_lengths(G, coords, list(G.edges()))
        else:
            weighted_edges = False

    # --- Generate unaltered (removal_amt == 0) and altered kathmandu odbc importance values up to ( final_removal_amt )
    # - ( G_vals_per_removal_amt ) of format dict[removal_amt][node] = criticality_val
    G_vals_per_removal_amt = TestHandler.calc_all_altered_odbc(G.copy(),
                                                               destinations=destinations,
                                                               increment=increment,
                                                               final_removal_amt=final_removal_amt,
                                                               pop_weights=node_pops_dict,
                                                               test_type=test_type,
                                                               samples=samples,
                                                               weighted_edges=weighted_edges)
    # =============================================================================================================== #

    # --- Normalize results of undisrupted and disrupted graph for calculations and visualization
    crit_vals_clean_norm = normalize_results(destinations, G_vals_per_removal_amt[0.0], 0, 1)
    crit_vals_disrupted_norm = normalize_results(destinations, G_vals_per_removal_amt[test_removal_amt], 0, 1)

    # --- Find diffs between orig odbc vals and altered odbc vals then normalize the diffs
    avg_odbc_diffs = calculations.calc_odbc_diffs(G, crit_vals_clean_norm, crit_vals_disrupted_norm)
    norm_avg_odbc_diffs = normalize_results(destinations, avg_odbc_diffs, -1, 1)

    # --- Create CMaps
    # destination orange for all cmaps
    if cmap_type == "log":
        cmap = graph_draw.create_log_cmap(nodes, destinations, crit_vals_disrupted_norm)
    elif cmap_type == "diff":
        cmap = graph_draw.create_avg_diffs_cmap(nodes, destinations, norm_avg_odbc_diffs)
    elif cmap_type == "gray":
        cmap = graph_draw.create_gray_cmap_with_destinations(nodes, destinations)
    else:
        print("Please input an allowable cmap_type.")
        cmap = None

    # --- Plot results
    plot_graph(G, [i * 100 for i in list(crit_vals_disrupted_norm.values())], cmap, coords)


if __name__ == '__main__':
    main()
