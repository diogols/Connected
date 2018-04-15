import networkx as nx
import matplotlib.pyplot as plt
from random import randint
import sys


def connected_graph(vertexes):
    connected = nx.Graph()
    connected.add_nodes_from(range(vertexes))
    is_connected = False
    while not is_connected:
        u = randint(0, vertexes-1)
        v = randint(0, vertexes-1)
        if not connected.has_edge(u, v) and u != v:
            connected.add_edge(u, v)
        is_connected = nx.is_connected(connected)
    return connected


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


n = int(sys.argv[1])
if n < 1:
    exit("You must at least insert one node.")
g = connected_graph(n)

# Tick 0: choose node
ticks = [-1 for x in range(n)]
chosen_one = randint(0, n - 1)
nodes = [chosen_one]
tick = 0
ticks[chosen_one] = tick
while not finished(ticks):
    tick += 1
    nodes = send(g, nodes, ticks, tick)

fig = plt.gcf()
fig.canvas.set_window_title('Broadcast with ' + str(n) + ' nodes')
fig_manager = plt.get_current_fig_manager()
fig_manager.full_screen_toggle()

l = array_to_matrix(ticks)
plt.xticks(range(max(ticks)+1))
if n < 30:
    plt.yticks(range(n))
for i in range(len(l)):
    for j in l[i]:
        plt.scatter([i], [j], color='blue')

plt.ylabel('Nodes')
plt.xlabel('Rounds')
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
plt.xlabel('Rounds')
plt.title('Broadcast on connected graph')
plt.show()
