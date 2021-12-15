def add_destinations_to_vals_vis(hospitals, odbc_vals):
    odbc_vals_with_destinations_maxed = {}
    for key, val in odbc_vals.items():
        if key in hospitals:
            odbc_vals_with_destinations_maxed[key] = max(odbc_vals)
        else:
            odbc_vals_with_destinations_maxed[key] = odbc_vals[key]
    return odbc_vals_with_destinations_maxed


# =============================================== Cmap handling ===================================================== #
def create_log_cmap(nodes, destinations, odbc_values):
    sorted_odbc_vals = sorted(odbc_values.items(), key=lambda x: x[1], reverse=False)

    len_nodes = len(nodes)
    p50 = sorted_odbc_vals[int(len_nodes * 0.5)][1]
    p75 = sorted_odbc_vals[int(len_nodes * 0.75)][1]
    p88 = sorted_odbc_vals[int(len_nodes * 0.88)][1]
    p95 = sorted_odbc_vals[int(len_nodes * 0.95)][1]
    p100 = sorted_odbc_vals[len_nodes - 1][1]

    print("log calc. values", p50, p75, p88, p95, p100)

    # create color map based off of logarithmic separation of data, then overwrite any outliers
    logarithmic_cmap = []
    for key, val in odbc_values.items():
        if key in destinations:
            logarithmic_cmap.append('orange')
            continue

        if val < p50:
            logarithmic_cmap.append("blue")
        elif p50 <= val < p75:
            logarithmic_cmap.append("green")
        elif p75 <= val < p88:
            logarithmic_cmap.append("yellow")
        elif p88 <= val < p95:
            logarithmic_cmap.append("red")
        elif val >= p95:
            logarithmic_cmap.append("black")
        else:
            # should never see any pink nodes, this signifies an error
            print("create_log_cmap: Log calc. error")
            logarithmic_cmap.append("pink")

    return logarithmic_cmap


def create_avg_diffs_cmap(nodes, destinations, avg_diffs):
    avg_diffs_cmap = []  # cmap to be returned
    for i in range(0, len(nodes)):
        if nodes[i] in destinations:
            avg_diffs_cmap.append('orange')
            continue

        if avg_diffs[i] < 0:
            avg_diffs_cmap.append('red')
        elif avg_diffs[i] == 0:
            avg_diffs_cmap.append('gray')
        elif avg_diffs[i] > 0:
            avg_diffs_cmap.append('purple')
    return avg_diffs_cmap


def create_thirds_cmap(destinations, odbc_vals):
    sorted_odbc_vals = sorted(odbc_vals.items(), key=lambda x: x[1], reverse=False)

    p33 = sorted_odbc_vals[int(0.33 * len(odbc_vals))][1]
    p66 = sorted_odbc_vals[int(0.66 * len(odbc_vals))][1]

    print(p33, p66)

    thirds_cmap = []
    for key, val in odbc_vals.items():
        if key in destinations:
            thirds_cmap.append('orange')

        if val < p33:
            thirds_cmap.append('green')
        elif p33 <= val < p66:
            thirds_cmap.append('yellow')
        elif val >= p66:
            thirds_cmap.append('red')
    return thirds_cmap


def create_gray_cmap_with_destinations(nodes, destinations):
    gray_cmap = []  # cmap to be returned
    for val in nodes:
        if val in destinations:
            gray_cmap.append('orange')
        else:
            gray_cmap.append('gray')
    return gray_cmap
