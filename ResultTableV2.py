# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:24:50 2020

@author: Haoran Wang
"""

import arcpy
import math
import numpy as np
import pandas as pd
from collections import Counter


#Get the data in the toolbar in the tool box
Origin  = arcpy.GetParameterAsText(0)   # Origin layer
Features  = arcpy.GetParameterAsText(1) # Characteristic variable field name
Destination  = arcpy.GetParameterAsText(2) # Destination layer


#Read the data in the toolbar
arcpy.AddMessage(Origin)
arcpy.AddMessage(Features)
arcpy.AddMessage(Destination)


#Create a Result Table
# Set workspace
arcpy.env.workspace = "F:/arcgis pro/Network-Construction/Network-Construction.gdb"
# Set local variables
out_path = "F:/arcgis pro/Network-Construction/Network-Construction.gdb"
out_name = "bbb"
tablepath = "F:/arcgis pro/Network-Construction/Network-Construction.gdb/bbb"
ResultTable = arcpy.management.CreateTable(out_path,out_name)


#Add new fields in the ResultTable
arcpy.management.AddField(ResultTable, "similarityIndex", "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
arcpy.management.AddField(ResultTable, "Origin", "SHORT", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
arcpy.management.AddField(ResultTable, "Destination", "SHORT", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)


#Create a read-only cursor for Origin
rows = arcpy.SearchCursor(Origin)
row = rows.next()


#The index of Origin field
OriginIndex = 1


while row:

    #Obtain the original attribute table data as the initial feature variable array
    ovset = Features.split(';')
    arcpy.AddMessage(ovset)


    #Establish the characteristic variable array of the origin
    #Generate two independent vest arrays to prepare for the sorting part of the algorithm
    vset1 = []
    vset2 = []
    for i in ovset:
        v = row.getValue(i)
        vset1.append(v)
        vset2.append(v)
    arcpy.AddMessage(vset1)


    #Create a read-only cursor for Destination
    rows1 = arcpy.SearchCursor(Destination)
    row1 = rows1.next()


    #Create an array to store the results
    resultSet = []


    #Establish an array of characteristic variables for comparing cities
    cset1 = []
    cset2 = []


    #The index of Destination field
    Destination_index = 0
    Destination_index2 = 1


    while row1:
        cset1 = []
        cset2 = []
        for j in ovset:
            
            v = row1.getValue(j)
            cset1.append(v)
            cset2.append(v)

        #Calculate the correlation coefficient and store it in the result array
        n = len(vset1)
        vset1.sort()
        cset1.sort()


        pr = np.ones((1,n))
        ps = np.ones((1,n))
        
        for i in range(n):
            #Get the rank statistics
            #The data is in the form of a list so we use this method, the array has another method
            #For a list of repeated elements, only the index of the first appearing element can be obtained, while the array can be obtained at one time, but the return of the array is tuple form
            pr[0][i] = vset1.index(vset2[i])
            ps[0][i] = cset1.index(cset2[i])                 
        
        def findrank(x1,z):
            #Get repeated elements    
            repeat =[item for item, count in Counter(vset1).items() if count > 1]
            #Get repetitions
            rcount = [count for item, count in Counter(vset1).items() if count > 1]
            nr = len(repeat)
            #Deal with the rank statistics of repeated elements      
            for j in range(nr):                          
                a = vset1.index(repeat[j])
                m = rcount[j]
                b = (m*a+(m-1)*m/2)/m
                [d,c] = np.where(z==a)
                z[0][c] = b
        
        findrank(vset1,pr) 
        findrank(cset1,ps)
        qxy = 0
        #Calculate Spearman's correlation coefficient
        for i in range(n):
            qxy = qxy + np.square(pr[0][i] - ps[0][i])                        
        qxy = 1 - 6/n/(np.square(n)-1)*qxy  
        #Adjust the correlation coefficient to between 0-2
        r = 1-qxy
        if math.isnan(r):
            r = 2
        
        #Write the result to the result list
        resultSet.append(r)

        row1 = rows1.next()

        #Write the calculation result into the new field of the ResultTable
        # Create insert cursor for table
        rows3 = arcpy.InsertCursor(tablepath)

        # Create new rows. Set the similarity values
        row3 = rows3.newRow()
        row3.setValue("similarityIndex", resultSet[Destination_index])
        row3.setValue("Destination", Destination_index2)
        row3.setValue("Origin", OriginIndex)
        rows3.insertRow(row3)
        Destination_index = Destination_index + 1
        Destination_index2 = Destination_index2 +1

        # Delete cursor and row objects to remove locks on the data
        del row3
        del rows3

    row = rows.next()
    #Delete old cursor

    del rows1
    del row1

    OriginIndex = OriginIndex + 1

del rows
del row







