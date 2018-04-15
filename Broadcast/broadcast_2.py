import networkx as nx
import matplotlib.pyplot as plt
from random import randint
import numpy as np
import sys


def connected_graph(vertexes):
    connected = nx.Graph()
    connected.add_nodes_from(range(vertexes))
    is_connected = False
    while not is_connected:
        u = randint(0, vertexes - 1)
        v = randint(0, vertexes - 1)
        if not connected.has_edge(u, v) and u != v:
            connected.add_edge(u, v)
        is_connected = nx.is_connected(connected)
    return connected


def add_edges(graph, percentage):
    if percentage < 0:
        percentage = 0
    edges = round(graph.number_of_edges() * percentage)
    while edges > 0:
        u = randint(0, graph.number_of_nodes() - 1)
        v = randint(0, graph.number_of_nodes() - 1)
        if not graph.has_edge(u, v) and u != v:
            graph.add_edge(u, v)
            edges -= 1
    return graph


def finished(array):
    for i in array:
        if i == -1:
            return False
    return True


def send(graph, u, rounds, r):
    result = []
    for node in u:
        for v in graph[node]:
            if rounds[v] == -1:
                rounds[v] = r
                result.append(v)
    return result


def array_to_matrix(l):
    result = [[] for _ in range((max(l) + 1))]
    for i in range(len(l)):
        result[l[i]].append(i)
    return result


def select(vertexes, probability):
    if probability < 0 or probability > 1:
        probability = 1
    mask = np.random.binomial(1, probability, len(vertexes))
    return [elem for keep, elem in zip(mask, vertexes) if keep]


n = int(sys.argv[1])
if n < 1:
    exit("You must insert at least one node.")
probability_edges = 1
probability_nodes = 0.4
g = add_edges(connected_graph(n), probability_edges)

# Tick 0: choose node
ticks = [-1 for x in range(n)]
old_ticks = list(ticks)
chosen_one = randint(0, n - 1)
nodes = [chosen_one]
tick = 0
ticks[chosen_one] = tick
while not finished(ticks) and not old_ticks == ticks:
    tick += 1
    print(ticks)
    old_ticks = list(ticks)
    nodes = select(nodes, probability_nodes)
    nodes = send(g, nodes, ticks, tick)
print(ticks)
fig = plt.gcf()
fig.canvas.set_window_title('Broadcast with' + str(n) + ' nodes')
fig_manager = plt.get_current_fig_manager()
fig_manager.full_screen_toggle()

l = array_to_matrix(ticks)
plt.xticks(range(max(ticks)+1))
if n < 30:
    plt.yticks(range(n))
for i in range(len(l)):
    for j in l[i]:
        plt.scatter([i], [j], color='blue')

plt.ylabel('Node')
plt.xlabel('Round')
plt.title('Broadcast on connected graph')
plt.show()

fig = plt.gcf()
fig.canvas.set_window_title('Broadcast with' + str(n) + ' nodes')
fig_manager = plt.get_current_fig_manager()
fig_manager.full_screen_toggle()
r = [len(x) for x in l]
plt.yticks(r)
plt.xticks(range(max(ticks)+1))
plt.plot(range(len(l)), r, color='blue')
plt.ylabel('Number of Nodes')
plt.xlabel('Round')
plt.title('Broadcast on connected graph')
plt.show()
