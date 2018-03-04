import networkx as nx
import matplotlib.pyplot as plt
from random import randint

connected = nx.Graph()
nodes = int(input("Insert number of nodes: "))
fig = plt.gcf()  # change window title
fig.canvas.set_window_title('Connected ' + str(nodes) + ' nodes')
connected.add_nodes_from([0, nodes])
isConnected = False
total_tries = 0
success_tries = 0
# bug: it doesn't bring the window to the front
manager = plt.get_current_fig_manager()
manager.window.state('zoomed')
while not isConnected:
    total_tries += 1
    u = randint(0, nodes)
    v = randint(0, nodes)
    if not connected.has_edge(u, v):
        connected.add_edge(u, v)
        success_tries += 1
        isConnected = nx.is_connected(connected)
        nx.draw(connected, with_labels=True)
        plt.pause(0.5)
        plt.clf()  # clean previous graph
nx.draw(connected, with_labels=True)
plt.show()
# bug: save blank image
# f = plt.gcf()
# f.savefig("nodes_" + str(nodes), bbox_inches='tight')
print(total_tries, success_tries)
