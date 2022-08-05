import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from copy import deepcopy


#####################################################
# THIS FILE MANAGES THE STRUCTURE OF THE FRAMEWORKS 
# DISPLAYED TO THE USER.
#####################################################


relations = []
def set_pos(G):
    global pos
    pos = nx.shell_layout(G)

def create_graph(all_relations, labelling, favoured_preferences):
    try:
        plt.close()
    except:
        pass
    global relations, pos
    if relations == all_relations:
        newFramework = False
    else:
        newFramework = True
        relations = deepcopy(all_relations)

    G = nx.DiGraph()
    G.add_edges_from(
        all_relations)
    print("SHOWING EDGES NOW")
    print(G.edges())
    edge_color_map = []
    for i in G.edges():
        if i in favoured_preferences:
            edge_color_map.append('orange')
        else:
            edge_color_map.append('black')
    in_args=labelling[0]
    out_args=labelling[1]
    undec_args=labelling[2]
    color_map = []

    for node in G:
        if node in in_args:
            color_map.append('lime')
        elif node in out_args:
            color_map.append('tomato')
        else:
            color_map.append('lightgrey')

    val_map = {'A': 1.0,
               'D': 0.5714285714285714,
               'H': 0.0}

    values = [val_map.get(node, 0.25) for node in G.nodes()]

    f = plt.figure(figsize=(5, 4))
    plt.axis('off')


    if newFramework:
        set_pos(G)



    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                           node_color = color_map, node_size = 500)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color=edge_color_map, arrows=True, arrowsize=20)
    return f
