#!/usr/bin/env python
# coding: utf-8

# In[4]:


import networkx as nx
import random as r
import osmnx as ox


# In[9]:


class facilities:  
    def __init__(self, R, d):  
        self.R = R  
        self.d = d
list = []  

#def facilitygraph1(north=41.9483,south=41.8766,east=-87.5734,west=-87.8130):
H = ox.graph_from_bbox(41.9483,41.8766,-87.5734,-87.8130, network_type='drive')
    
for i in H.edges:
    if 'facilitynum' not in  H.edges[i[0],i[1],i[2]]:
        length=H.edges[i[0],i[1],i[2]]['length']
        if(22>length):
            k=(int)(length)
        else:
            k=22
        n=r.randint(0,k)
        H.edges[i[0],i[1],i[2]]['facilitynum']=n
            
        facilities_dist=r.sample(range(0,(int)(length*100)),n)
        facilities_dist.sort()
        facilities1=[x/100 for x in facilities_dist]
        H.edges[i[0],i[1],i[2]]['facilitydist']=facilities1
        for j in facilities1:
            list.append(facilities(r.randint(0,500),j))
               
            
        if [i[1],i[0],i[2]] in H.edges:
            H.edges[i[1],i[0],i[2]]['facilitynum']=n
            facilities2=[((int)((length-x)*100))/100 for x in facilities1]
            facilities2.sort()
            H.edges[i[1],i[0],i[2]]['facilitdist']=facilities2
            for k in facilities2:
                list.append(facilities(r.randint(0,500),k))       
                
        H.edges[i[0],i[1],i[2]]['length']=(int)(length*100)/100
    #H.edges(data=True,keys=True)
for obj in list: 
    print( obj.R, obj.d, sep =' , ' ) 
    
    #return H
        


# In[ ]:




