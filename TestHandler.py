import networkx
import random

from betweenness import betweenness_centrality_source

''' ================================================ Test Handling Methods ============================================= '''


def calc_single_sample_altered_odbc(G, destinations, removal_amt, samples, test_type="simp", pop_weights=None,
                                    weighted_edges=False):
    # used to keep track of avg values found after multiple sample test, single removal amount, list
    avg_values = {}
    # clear avg_values before each test is performed
    for val in list(G.nodes()):
        avg_values[val] = 0

    # create temp graph for testing, calc. removal_size using curr_removal_amt, selected edges to be removed using
    # removal size, and finally call calc_single_sample_altered_odbc to find avg_values for sample
    for i in range(0, samples):
        # print("Current simulation:", i)

        # create copy of kathmandu graph to disrupt
        alt_G = G.copy()

        ################## remove percent of edges using curr_removal_amt randomly ###################
        # calc. # of edges to remove
        removal_size = int(len(alt_G.nodes()) * removal_amt)
        # designate which nodes to be removed, randomly
        edges_to_be_removed = random.sample(G.edges(), k=removal_size)
        # remove selected edges to be removed from temp graph
        alt_G.remove_edges_from(edges_to_be_removed)
        ##############################################################################################

        # init. dict. for storage of criticality vals
        new_odbc_values = {}

        # perform odbc testing for simulation
        ################# each iteration create new_odbc_values with disrupted kathmandu network ###########################
        if test_type == "simp":  # simple ODBC
            new_odbc_values = networkx.betweenness_centrality_source(alt_G, sources=destinations)
        elif test_type == "bc":  # performs regular betweeness centrality metric
            new_odbc_values = networkx.betweenness_centrality(alt_G)
        else:  # all tests created by us ("dist", "pop", "dist&pop (NOT FINISHED)")
            new_odbc_values = betweenness_centrality_source(alt_G, test_type, pop_weights=pop_weights,
                                                            weighted_edges=weighted_edges, sources=destinations)
        ####################################################################################################################

        # add new_odbc_vales to avg_values
        for key, val in avg_values.items():
            if key in new_odbc_values:
                avg_values[key] += new_odbc_values[key]

    return avg_values


def calc_all_altered_odbc(G, destinations, increment, final_removal_amt, pop_weights, test_type, samples,
                          weighted_edges=False):
    # init. curr_removal_amt var. to 0
    curr_removal_amt = 0

    # used to keep track of avg values found after multiple sample test, all removal amounts, dict
    avg_vals_per_remov_amt = {}

    # tests performed for removal amounts in increments designated up to final_removal_amt, with # of samples=samples
    while curr_removal_amt <= final_removal_amt:
        print("Current % removal amount:", round(curr_removal_amt, 2))  # for debugging, comment out if not necessary

        avg_values = calc_single_sample_altered_odbc(G.copy(), destinations, round(curr_removal_amt, 2), samples,
                                                     test_type=test_type, pop_weights=pop_weights,
                                                     weighted_edges=weighted_edges)

        # using values stored in avg_values find the actual averages by dividing by # of samples
        for key, val in avg_values.items():
            avg_values[key] = val / samples

        # append avg_values to dictionary
        avg_vals_per_remov_amt[round(curr_removal_amt, 2)] = avg_values.copy()

        # add increment to curr_removal_amt for next test
        curr_removal_amt += increment

    return avg_vals_per_remov_amt