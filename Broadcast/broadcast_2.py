import networkx as nx
import matplotlib.pyplot as plt
from random import randint
import numpy as np
import argparse


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


def send(graph, u, rounds, r, probability):
    result = []
    for node in u:
        for v in select([x for x in graph[node]], probability):
            if rounds[v] == -1:
                rounds[v] = r
                result.append(v)
    return result


def array_to_matrix(l):
    result = [[] for _ in range((max(l) + 1))]
    for i in range(len(l)):
        if l[i] != -1:
            result[l[i]].append(i)
    return result


def select(vertexes, probability):
    mask = np.random.binomial(1, probability, len(vertexes))
    result = [elem for keep, elem in zip(mask, vertexes) if keep]
    if not result:
        result.append(vertexes[0])
    return result


def unsigned_int(arg):
    v = int(arg)
    if v < 0:
        raise argparse.ArgumentTypeError('The value has to be higher than 1.')
    return v


def percentage_float(arg):
    v = float(arg)
    if v < 0 or v > 1:
        raise argparse.ArgumentTypeError('Value has to be between 0 and 1.')
    return v


def low_percentage_float(arg):
    v = float(arg)
    if v < 0:
        raise argparse.ArgumentTypeError('Value has to be higher than 0')
    return v


parser = argparse.ArgumentParser()
parser.add_argument("-v",  type=unsigned_int, help="Number of nodes.", default=10)
parser.add_argument("-n",  type=percentage_float, help="Percentage of nodes.", default=1)
parser.add_argument("-e",  type=low_percentage_float, help="Percentage of edges.", default=1)
args = parser.parse_args()

n = args.v
probability_edges = args.e
probability_nodes = args.n
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
    old_ticks = list(ticks)
    nodes = send(g, nodes, ticks, tick, probability_nodes)
print(ticks)
l = array_to_matrix(ticks)
print(l)
fig = plt.gcf()
fig.canvas.set_window_title('Broadcast with ' + str(n) + ' nodes')
fig_manager = plt.get_current_fig_manager()
fig_manager.full_screen_toggle()
r = [len(x) for x in l]
plt.yticks(r)
plt.xticks(range(max(ticks)+1))
plt.plot(range(len(l)), r, color='blue')
plt.ylabel('Number of Nodes')
plt.xlabel('Round')
title = 'Broadcast: %d of %d nodes received the message' % (np.sum([len(x) for x in l]),  n)
plt.title(title)
plt.show()
