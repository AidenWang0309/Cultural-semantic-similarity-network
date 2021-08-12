# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 10:29:59 2021

@author: Haoran Wang
"""
import networkx as nx
import random
import string
import csv
import xlrd
import xlwt

#G=nx.karate_club_graph()
"""Construct a graph"""
# open the excle table
data = xlrd.open_workbook('C:/Users/Lenovo/Desktop/ODTable0.1V2.xlsx')

# read sheet names of the table
data.sheet_names()
print("sheets：" + str(data.sheet_names()))

# get the Sheet1 by name
table = data.sheet_by_name('Sheet1')

# Print data.sheet_names() to find that the returned value is a list, and worksheet 1 is obtained by indexing the list.
# table = data.sheet_by_index(0)

# Get the number of rows and columns
# Number of rows: table.nrows
# Number of columns: table.ncols
print("Total number of rows:" + str(table.nrows))
print("Total number of columns:" + str(table.ncols))

G = nx.Graph()  # construct a undirected graph
# G = nx.DiGraph() #construct a directed graph
TableNR = table.nrows
TableNR2 = TableNR + 1
for i in range(TableNR):
    list1 = table.row_values(i)
    G.add_weighted_edges_from([(list1[2],list1[3],list1[11])])


from networkx.algorithms import community
def label_propagation_community(G):
    communities_generator = list(community.label_propagation_communities(G))
    m = []
    for i in communities_generator:
        m.append(list(i))
    return m

g=label_propagation_community(G)
print(g)
