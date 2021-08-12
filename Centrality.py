# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 09:43:37 2021

@author: Haoran Wang
"""

import random
import string
import csv
import xlrd
import xlwt
import networkx as nx
import matplotlib.pyplot as plt

"""Construct a graph"""
# open the excle table
# Change the path of the OD table file according to user needs
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
print("rows:" + str(table.nrows))
print("columns:" + str(table.ncols))

# G = nx.Graph()  # construct a undirected graph
G = nx.DiGraph()  # construct a directed graph
TableNR = table.nrows
TableNR2 = TableNR + 1
for i in range(TableNR):
    list1 = table.row_values(i)
    G.add_weighted_edges_from([(list1[2], list1[3], list1[11])])

# Note that the suffix of the excel file here is xls.
# If it is opened by xlsx, it will prompt invalid.
# After creating a new excel table, select the text format to save
all_str = string.ascii_letters + string.digits
excelpath = ('C:/Users/Lenovo/Desktop/EC.xls')  # New excel file
workbook = xlwt.Workbook(encoding='utf-8')  # Write to excel file
sheet = workbook.add_sheet('Sheet1',cell_overwrite_ok=True)  # Add a sheet
headlist = [u'PointID', u'EigenvectorCentrality']   # Write data header
row = 0
col = 0
for head in headlist:
    sheet.write(row, col, head)
    col = col+1
for i in range(1, TableNR2):  # Write TableN2 row data
    for j in range(1, 2):  # Write 3 columns of data
        bet_cen = nx.betweenness_centrality(G)
        # clo_cen = nx.closeness_centrality(G)
        eig_cen = nx.eigenvector_centrality(G)
        # deg_cen = nx.degree_centrality(G)
        listID = list(bet_cen.keys())  # Get the number of nodes
        # listBC = list(bet_cen.values())
        # listCC = list(clo_cen.values())
        listEC = list(eig_cen.values())
        # listDC = list(deg_cen.values())
        sheet.write(i, j-1, listID[i-1])
        sheet.write(i, j, listEC[i-1])
        # sheet.write(i,j+1,listCC[i-1])
        # sheet.write(i,j+2,listEC[i-1])
        # sheet.write(i,j+3,listDC[i-1])

    workbook.save(excelpath)  # Save


