import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx

def plot_base_graph(G, color, coords):
    plt.figure(3, figsize=(100, 100))
    networkx.draw(G, node_size=80, node_color=color, pos=coords)
    plt.savefig("updated_res_images/updated03/kath_pop_orig_odbc_0.png", format="PNG")
    plt.show()


def plot_graph_disrupted(G, node_sizes, cmap, coords):
    plt.figure(3, figsize=(100, 100))

    # legend creation
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='95th-100th Percentile',
                              markerfacecolor='black', markersize=90),
                       Line2D([0], [0], marker='o', color='w', label='88th-95th Percentile',
                              markerfacecolor='red', markersize=90),
                       Line2D([0], [0], marker='o', color='w', label='75th-88th Percentile',
                              markerfacecolor='yellow', markersize=90),
                       Line2D([0], [0], marker='o', color='w', label='50th-75th Percentile',
                              markerfacecolor='green', markersize=90),
                       Line2D([0], [0], marker='o', color='w', label='0-50th Percentile',
                              markerfacecolor='blue', markersize=90)]
    plt.legend(handles=legend_elements, title="Node Color Legend", title_fontsize=120, loc='upper left',
               prop={'size': 90})
    # map scale bar creation
    #scalebar = ScaleBar(0.85, location='lower right', font_properties={'size': 100})  # 1 pixel = 0.2 meter
    #plt.gca().add_artist(scalebar)

    # network drawing
    networkx.draw(G, node_size=node_sizes, node_color=cmap, pos=coords)
    plt.savefig("updated_res_images/updated03/kath_pop_alt_odbc_05.png", format="PNG")
    plt.show()