import networkx as nx
import matplotlib.pyplot as plt
from random import randint

nodes = int(input("Number of maximum nodes: "))
fig = plt.gcf()  # change window title
fig.canvas.set_window_title('Plot ' + str(nodes) + ' nodes')
# bug: it doesn't bring the window to the front
fig_manager = plt.get_current_fig_manager()
fig_manager.full_screen_toggle()
var = 1
x = []
y = []
while var < nodes:
    connected = nx.Graph()
    connected.add_nodes_from(range(0, var))
    isConnected = False
    success_tries = 0
    while not isConnected:
        u = randint(0, nodes)
        v = randint(0, nodes)
        if not connected.has_edge(u, v) and not u == v:
            connected.add_edge(u, v)
            success_tries += 1
            isConnected = nx.is_connected(connected)
    x.append(var)
    y.append(success_tries)
    var += 5
plt.plot(x, y)
plt.ylabel('Edges')
plt.xlabel('Nodes')
plt.title('Random Connected Graph')
plt.show()
