#!/usr/bin/env python
# coding: utf-8

# In[22]:


import networkx as nx
import random as r
import osmnx as ox


# In[101]:


def facilitygraph(north=41.9483,south=41.8766,east=-87.5734,west=-87.8130):

#north, south, east, west = 41.9483, 41.6766, -87.5734, -87.8130

    H = ox.graph_from_bbox(north, south, east, west, network_type='drive')
    
    for i in H.edges:
        if 'facilitynum' not in  H.edges[i[0],i[1],i[2]]:
            length=H.edges[i[0],i[1],i[2]]['length']
            if(22>length):
                k=(int)(length)
            else:
                k=22
            n=r.randint(0,k)
            H.edges[i[0],i[1],i[2]]['facilitynum']=n
            
            facilities=r.sample(range(0,(int)(length*100)),n)
            facilities.sort()
            facilities1=[x/100 for x in facilities]
            H.edges[i[0],i[1],i[2]]['facilitdist']=facilities1
            
            
            if [i[1],i[0],i[2]] in H.edges:
                H.edges[i[1],i[0],i[2]]['facilitynum']=n
                facilities2=[((int)((length-x)*100))/100 for x in facilities1]
                facilities2.sort()
                H.edges[i[1],i[0],i[2]]['facilitdist']=facilities2
                
                
            H.edges[i[0],i[1],i[2]]['length']=(int)(length*100)/100
    #H.edges(data=True,keys=True)

    
    return H





#H.adj[261094125]#[261094125][0]['length']
    


# In[58]:


#cars=r.sample(range(0,(int)(28.256*100)),6)
#cars.sort()
#cars=[x/100 for x in cars]
#print(cars)


# In[ ]:




