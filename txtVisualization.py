import csv
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


# 生成关系图

def file2array(path, delimiter=' '):
    fp = open(path, 'r', encoding='utf-8')
    string = fp.read()
    fp.close()
    row_list = string.splitlines()
    data_list = [[int(i) for i in row.strip().split(delimiter)] for row in row_list]
    return np.array(data_list)


def loadGraph(graph_name):
    with open('C:/Game/{}_node.csv'.format(graph_name), 'r',
              encoding='utf-8') as fp:
        reader = csv.reader(fp)
        nodes = list(int(_[0]) for _ in reader)
    with open('C:/Game/{}_edge.csv'.format(graph_name), 'r',
              encoding='utf-8') as fp:
        reader = csv.reader(fp)
        edges = list((int(_[0]), int(_[1])) for _ in reader if _[0] != _[1])
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G


# 利用清洗后的id字典生成无向图
dataset = 'graph'
txt_address = 'C:/Game/{}.txt'.format(dataset)

data2array = file2array(txt_address)
data1array = list(np.array(data2array).flatten())
data1array = list(set(data1array))

csv_node_address = 'C:/Game/{}_node.csv'.format(dataset)
np.savetxt(csv_node_address, data1array, delimiter='\n', fmt='%d')

csv_edge_address = 'C:/Game/{}_edge.csv'.format(dataset)
with open(csv_edge_address, 'w+', newline='') as csvfile:
    spamriter = csv.writer(csvfile, dialect='excel')
    with open(txt_address, 'r', encoding='utf-8') as filein:
        for line in filein:
            line_list = line.strip('\n').split(' ')
            spamriter.writerow(line_list)
csvfile.close()

G = loadGraph(dataset)
pos = nx.spring_layout(G)
np.save('C:/Game/{}_pos.npy'.format(dataset), pos)
nx.draw(G, pos, nodelist=G.nodes(), node_color='y', node_size=2, width=0.05)
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.savefig("Visualization.png")
plt.savefig("Visualization.svg")
plt.show()

