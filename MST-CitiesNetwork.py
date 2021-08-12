# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 17:17:19 2021

@author: Haoran Wang
"""

import matplotlib.pyplot as plt
import networkx as nx
import xlrd

# open the excle table
data = xlrd.open_workbook('C:/Users/Lenovo/Desktop/OTAdistance.xlsx')

# read sheet names of the table
data.sheet_names()
print("sheets：" + str(data.sheet_names()))

# get the Sheet1 by name
table = data.sheet_by_name('Sheet1')

# Print data.sheet_names() to find that the returned value is a list,
# and worksheet 1 is obtained by indexing the list.
# table = data.sheet_by_index(0)

# Get the number of rows and columns
# Number of rows: table.nrows
# Number of columns: table.ncols
print("rows:" + str(table.nrows))
print("columns: " + str(table.ncols))

G = nx.Graph()  # construct a undirected graph
# G = nx.DiGraph() #construct a directed graph
TableNR = table.nrows
TableNR2 = TableNR + 1
for i in range(TableNR):
    list1 = table.row_values(i)
    G.add_weighted_edges_from([(list1[8],list1[11],list1[1])])
    

def draw(g):
 pos = nx.spring_layout(g)
 nx.draw(g, pos, \
   arrows=True, \
   with_labels=True, \
   nodelist=g.nodes(), \
   style='dashed', \
   edge_color='b', \
   width=2, \
   node_color='y', \
   alpha=0.5)
 plt.show()
 # Solve the problem that Chinese cannot be displayed
 plt.rcParams['font.sans-serif']=['SimHei']
 plt.rcParams['axes.unicode_minus'] = False




def prim(G, s):
 dist = {}  # dist records the minimum distance to the node
 parent = {}  # parent records the parent table of the minimum spanning tree
 Q = list(G.nodes())  # Q contains all nodes not covered by the spanning tree
 MAXDIST = 9999.99  # MAXDIST means positive infinity, that is, two nodes are not adjacent
 # Initialization data
 # The minimum distance of all nodes is set to MAXDIST, and the parent node is set to None
 for v in G.nodes():
  dist[v] = MAXDIST
  parent[v] = None
 # The distance to the starting node s is set to 0
 dist[s] = 0
 # Keep taking out the "nearest" node from Q and adding it to the minimum spanning tree
 # Stop the loop when Q is empty, and the algorithm ends
 while Q:
  # Take out the "nearest" node u and add u to the minimum spanning tree
  u = Q[0]
  for v in Q:
   if (dist[v] < dist[u]):
    u = v
  Q.remove(u)
  # Update the minimum distance of u's adjacent nodes
  for v in G.adj[u]:
   if (v in Q) and (G[u][v]['weight'] < dist[v]):
    parent[v] = u
    dist[v] = G[u][v]['weight']
 # The algorithm ends, and the minimum spanning tree is returned in the form of a parent table
 return parent


tree = prim(G, 1)
mtg = nx.Graph()
mtg.add_edges_from(tree.items())
mtg.remove_node(None)
draw(mtg)
