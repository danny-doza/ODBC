import math


def calc_odbc_diffs(kathmandu, orig_odbc_vals_dict, alt_odbc_vals_dict):
    odbc_diffs_dict = {}
    for val in list(kathmandu.nodes()):
        odbc_diffs_dict[val] = 0

    for key, val in orig_odbc_vals_dict.items():
        odbc_diffs_dict[key] = orig_odbc_vals_dict[key] - alt_odbc_vals_dict[key]

    return odbc_diffs_dict

# def calc_edge_importances(kathmandu, avg_values_list):
#     # create usable list of edge tuples
#     edge_list = list(kathmandu.edges())
#     # initialize odbc val edges dict
#     calculated_odbc_edge_vals = {}
#     for val in edge_list:
#         calculated_odbc_edge_vals[val] = -1

#     # creat dict with edges as key and edge importance as val
#     for val in edge_list:
#         # get odbc importance of nodes at either end of edge and take their average to create importance val for edge
#         calculated_odbc_edge_vals[val] = (avg_values_list[val[0]] + avg_values_list[val[1]])/2

#     return calculated_odbc_edge_vals


def calc_edge_lengths(kathmandu, node_positions, edges):
    edge_weight_dict = {}

    for edge in edges:
        kathmandu[edge[0]][edge[1]]['weight'] = math.sqrt(
            (node_positions[edge[1]][0] - node_positions[edge[0]][0]) ** 2 + (
                        node_positions[edge[1]][1] - node_positions[edge[0]][1]) ** 2)
    return True
