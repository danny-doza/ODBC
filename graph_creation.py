# ============================= Graph adjacency list creation (Kathmandu) ======================================== #
def file_len(fname):  # helper function to return length of file (number of nodes)
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


# creates adjacency list from kathmandu csv file for use in creation of Networkx graph
def create_adjacency_list(filename):  # use filename = 'r"kathii_wei.txt"'
    kat_dict = {}

    file = open(filename)  # create file obj.
    kat = [[]] * file_len(filename)  # list of lists to be given each point and it's neighbors along with edge weights
    node_count = 0  # line number = node number = node_count
    for line in file:
        line = line.split()  # line[0] = node num. pt. 1, line[1] = node num. pt. 2, line[2] = edge weight
        kat[node_count] = [int(line[0]), int(line[1]), float(line[2])]
        node_count += 1  # increment node num.

    for i in range(0, len(kat)):
        if kat[i][0] in kat_dict:  # if node num. has already been encountered
            if kat[i][1] in kat_dict[kat[i][0]]:
                kat_dict[kat[i][0]][kat[i][1]]['weight'] = kat[i][2]
            else:
                kat_dict[kat[i][0]][kat[i][1]] = {}
                kat_dict[kat[i][0]][kat[i][1]]['weight'] = kat[i][2]
        # if it has not been encountered initialize the points with dicts and create edge weight between
        # kat[i][0] and kat[i][1]
        else:
            kat_dict[kat[i][0]] = {}
            kat_dict[kat[i][0]][kat[i][1]] = {}
            kat_dict[kat[i][0]][kat[i][1]]['weight'] = kat[i][2]

    return kat_dict


# ================================= Coordinate dict. creation handling for visualization ============================= #
# coordinate creation for lattice network
def init_lattice_coords(nodes):
    # positions used to make sure drawn graph is flat, that's all
    coords = {}
    for node in nodes:
        coords[node] = node
    return coords


# coordinate creation for kathmandu network
def init_coords(filename, nodes):  # use filename = "kathiicoord_original.txt"
    coords = {}  # init. our coords dict to be returned

    file = open(filename)  # create file obj
    node_count = 1  # line number = node number = node_count
    for line in file:
        line = line.split()  # line[0] = node num. x value, line[1] = node num. y value
        # if node number is not in the returned kathmandu nodes, do not bother adding it to coords
        if node_count in nodes:
            coords[node_count] = [float(line[0]), float(line[1])]  # add node num. to coords dict == [coord x, coord y]
        node_count += 1  # increment our node num.

    return coords
