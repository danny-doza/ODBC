# ============================================= Population Handling ================================================== #
def calc_node_pops(filename_ward_d, filename_voronoi_d):
    file_ward_data = open(filename_ward_d)
    file_voronoi_data = open(filename_voronoi_d)

    # used to determine ward total populations
    ward_pops = []
    # ward polygon area
    ward_areas = []
    # ward id, used to determine which voronoi polygons corresponds to ward
    ward_ids = []

    ward_id_pop_dict = {}

    ward_data_fields = file_ward_data.readline()
    for line in file_ward_data:
        split_line = line.split(',')
        ward_pop = split_line[20].strip('\"')
        ward_area = split_line[21].strip('\"')
        ward_id = split_line[22].strip('\"')

        ward_pops.append(ward_pop)
        ward_areas.append(ward_areas)
        ward_ids.append(ward_ids)

        ward_id_pop_dict[ward_id] = [ward_pop, ward_area]

    # used to determine which node inside kathmandu network voronoi poly corresponds to
    voronoi_node_nums = []
    # voronoi polygon area
    voronoi_areas = []
    # corresponding to which ward voronoi polygon is in
    voronoi_ward_ids = []

    voronoi_data_fields = file_voronoi_data.readline()
    for line in file_voronoi_data:
        split_line = line.split(',')
        voronoi_node_num = split_line[0].strip('\"')
        voronoi_area = split_line[2].strip('\"')
        voronoi_ward_id = split_line[3].strip('\"')

        voronoi_node_nums.append(voronoi_node_num)
        voronoi_areas.append(voronoi_area)
        voronoi_ward_ids.append(voronoi_ward_id)

    # dictionary to be populated with node population data. {node: pop}
    voronoi_node_pops_dict = {}
    for i in range(0, len(voronoi_areas)):
        # 0: ward_pop, 1: ward_area
        ward_info_list = ward_id_pop_dict.get(voronoi_ward_ids[i], None)
        voronoi_percentage_wrt_ward_area = int(voronoi_areas[i]) / int(ward_info_list[1])
        calculated_pop = float(voronoi_percentage_wrt_ward_area) * float(ward_info_list[0])
        voronoi_node_pops_dict[voronoi_node_nums[i]] = calculated_pop

    return voronoi_node_pops_dict


# ======================================== Lattice population handling ============================================== #
def create_lat_node_pop_dict(lattice_nodes, pop_values):
    node_pops_dict = {}
    for i in range(0, len(lattice_nodes)):
        node_pops_dict[lattice_nodes[i]] = pop_values[i]
    return node_pops_dict


# ======================================= Kathmandu population handling ============================================= #
def create_kat_node_pop_dict(nodes):
    node_pops_dict = calc_node_pops('ward_data.csv', 'voronoi_data.csv')
    node_pops_sorted = sorted(node_pops_dict.items(), key=lambda x: x[0], reverse=False)

    node_pops_corrected_nodes = {}
    for i in range(0, len(node_pops_sorted)):
        node_pops_corrected_nodes[nodes[i]] = node_pops_sorted[i][1]

    print(node_pops_corrected_nodes)
    print(min(node_pops_corrected_nodes.values()), max(node_pops_corrected_nodes.values()))

    return node_pops_corrected_nodes
