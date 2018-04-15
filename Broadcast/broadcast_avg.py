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


# TODO: improve this function
def preferential_graph(vertexes, percentage):
    preferential = nx.Graph()
    preferential.add_nodes_from(range(vertexes))
    initial = np.full(vertexes, 1)
    degrees = np.full(vertexes, 1)
    is_connected = False
    while not is_connected:
        u = calculate(initial)
        v = calculate(degrees)
        if not preferential.has_edge(u, v) and not u == v:
            preferential.add_edge(u, v)
            degrees[v] += 1
            is_connected = nx.is_connected(preferential)
    edges = round(preferential.number_of_edges() * percentage)
    while edges > 0:
        u = calculate(initial)
        v = calculate(degrees)
        if not preferential.has_edge(u, v) and u != v:
            preferential.add_edge(u, v)
            degrees[v] += 1
            edges -= 1
    return preferential


def calculate(degree_array):
    total = sum(degree_array)
    size = len(degree_array)
    result = [None] * size
    for i in range(0, size):
        result[i] = degree_array[i]/total
    return np.random.choice(np.arange(0, size), p=result)


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


def send(graph, u, rounds, last, probability):
    result = []
    for node in u:
        for v in select([x for x in graph[node]], probability):
            if rounds[v] == -1:
                rounds[v] = last
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


def positive_int(arg):
    v = int(arg)
    if v < 1:
        raise argparse.ArgumentTypeError('Value has to be higher than 1')
    return v


def enumerate_char(arg):
    if not (arg == "c" or arg == "p"):
        raise argparse.ArgumentTypeError("Value has to be 'c' or 'p'")
    return arg


def sum_to_array(destiny, origin):
    length = len(destiny)
    while length < len(origin):
        destiny.append(0)
        length += 1
    for i in range(len(origin)):
        destiny[i] += origin[i]
    return destiny


parser = argparse.ArgumentParser()
parser.add_argument("-v",  type=unsigned_int, help="Number of nodes.", default=10)
parser.add_argument("-n",  type=percentage_float, help="Percentage of nodes.", default=1)
parser.add_argument("-e",  type=low_percentage_float, help="Percentage of edges.", default=1)
parser.add_argument("-r",  type=positive_int, help="Number of runs.", default=1)
parser.add_argument("-t", type=enumerate_char, help="Type of graph.", default="c")
args = parser.parse_args()

n = args.v
probability_edges = args.e
probability_nodes = args.n
runs = args.r

average = []
average_nodes = 0
average_rounds = 0
while runs > 0:
    if args.t == 'c':
        g = add_edges(connected_graph(n), probability_edges)
    else:
        g = preferential_graph(n, probability_edges)

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
    runs -= 1
    converted = [len(x) for x in array_to_matrix(ticks)]
    average = sum_to_array(average, converted)
    average_nodes += np.sum(converted)
    average_rounds += tick

fig = plt.gcf()
fig.canvas.set_window_title('Broadcast: ' + str(n) + ' nodes')
fig_manager = plt.get_current_fig_manager()
fig_manager.full_screen_toggle()
r = [x / args.r for x in average]
plt.yticks(r)
plt.xticks(range(len(average)))
plt.plot(range(len(average)), r, color='blue')
plt.ylabel('Average of Nodes')
plt.xlabel('Rounds (average = %.2f)' % (average_rounds / args.r))
title = 'Broadcast: %.2f of %d nodes received the message' % (average_nodes / args.r,  n)
plt.title(title)
plt.show()
