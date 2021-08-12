# Cultural-semantic-similarity-network
### Overview
This github project provides readers 3 datasets, 2 ArcgisPro toolboxes, and 5 codes, which are ***Cultural semantics of Chinese cities.zip***, ***ODTable-Git.xlsx***, ***OTAdistance-Git.xlsx***, ***ArcPy_Demo.tbx***, ***Network-Construction.tbx***, ***ResultTableV2.py***, ***odline.py***, ***Centrality.py***, ***LPA.py***, and ***MST-CitiesNetwork***. The following content will introduce their founction one by one.  
### Cultural semantics of Chinese cities.zip
The compressed file contains a Chinese cities shapefile with cultural semantics. Each city is defined with a ***9-dimensional cultrual eigenvetor***. It is the most important data basis in this study.  
### Network-Construction.tbx and ResultTableV2.
This tool can calculate the cultural similarity among cities based on ***Cultural semantic of Chinese cities***, and construct a ***Cultural Semantic Similarity Network*** OD Table.
### ArcPy_Demo.tbx and odline.py
This tool can be used to visualize the ***Network Origin-Destination Table*** in ArcGIS Pro.  
### ODTable-Git.xlsx
***ODTable-Git.xlsx*** is the calculation result of ***Network-Construction.tbx***. Users can calculate the centrality, paths, and communities based on it.  
### OTAdistance-Git.xlsx
It is an OD Table composed of physical distance among Chinese cities.
### Centrality.py, LPA.py, MST-CitiesNetwork.py
They can be used to calculate the centrality and communities based on ***ODTable-Git.xlsx*** and ***OTAdistance-Git.xlsx***.
