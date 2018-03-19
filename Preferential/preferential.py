import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from random import randint
from collections import Counter


def calculate(degree_array):
    total = sum(degree_array)
    size = len(degree_array)
    result = [None] * size
    for i in range(0, size):
        result[i] = degree_array[i]/total
    return np.random.choice(np.arange(0, size), p=result)


def random(degree_array):
    node = degree_array[randint(0, len(degree_array) - 1)]
    degree_array.append(node)
    return degree_array, node


graph = nx.Graph()
nodes = int(input("Insert number of nodes: "))
fig = plt.gcf()  # change window title
fig.canvas.set_window_title('Preferential ' + str(nodes) + ' nodes')
graph.add_nodes_from(range(0, nodes))
isConnected = False
fig_manager = plt.get_current_fig_manager()
fig_manager.full_screen_toggle()
# initialize arrays of the node degree and normalized probability
initial = np.full(nodes, 1)
degrees = np.full(nodes, 1)
# array = list(range(0, nodes))
# start algorithm
while not isConnected:
    # assume origin node u has weights of 1 on each node
    u = calculate(initial)
    v = calculate(degrees)
    # array, v = random(array)
    if not graph.has_edge(u, v) and not u == v:
        graph.add_edge(u, v)
        degrees[v] += 1
        isConnected = nx.is_connected(graph)

sorted_by_degree = sorted(graph.degree(), key=lambda var: var[1], reverse=True)
x, height = zip(*sorted_by_degree)
plt.subplot(1, 2, 1)
y = list(height)
plt.ylabel('Degree')
plt.xlabel('Node [INCORRECT NODE LABEL]')
plt.title('Preferential attachment')
# plt.xticks(x, x, rotation='vertical')
plt.bar(range(nodes), y, align='center', color='b')
plt.tight_layout()

plt.subplot(1, 2, 2)
pos = nx.circular_layout(graph)
nx.draw(graph, pos, with_labels=False, node_size=50, node_color='r', edge_color='b', width=0.9, alpha=0.7)
plt.show()

fig = plt.gcf()
fig.canvas.set_window_title('Preferential ' + str(nodes) + ' nodes')
graph.add_nodes_from(range(0, nodes))
fig_manager = plt.get_current_fig_manager()
fig_manager.full_screen_toggle()
plt.subplot(1, 2, 1)
stats = Counter(degrees).most_common()
degree = []
number = []
for d, n in stats:
    degree.append(d)
    number.append(n)
degree.reverse()
number.reverse()
y_pos = np.arange(len(number))
plt.bar(y_pos, degree, align='center')
plt.xticks(y_pos, number)
plt.ylabel('Degree')
plt.xlabel('# of nodes')
plt.title('Degree Distribution')
plt.subplot(1, 2, 2)
y_pos = np.arange(len(number))
plt.plot(y_pos, degree)
plt.xticks(y_pos, number)
plt.ylabel('log(Degree)')
plt.xlabel('log(# of nodes)')
plt.title('Degree Distribution log-log')
plt.yscale('log')
plt.xscale('log')
plt.show()
