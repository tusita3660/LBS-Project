#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import osmnx as ox
from Facility import *
import networkx as nx
from constants import *


# In[ ]:


class Advertisement:
    def __init__(self):
        self.G=ox.graph_from_bbox(north, south, east, west, network_type='drive')
        self.G=nx.convert_node_labels_to_integers(self.G) 
        self.all_pair_short()
        self.add_structure() 
    def all_pair_short(self):
        self.paths=[]
        for i in self.G.nodes:
            self.paths.append(nx.single_source_dijkstra_path_length(self.G,i,weight='length',cutoff=50000))
    def add_structure(self):
        for u,v,n in self.G.edges:
            self.G.edges[u,v,n]['Facilities']=[]
            self.G.edges[u,v,n]['relevant']={}
            self.G.edges[u,v,n]['relevantR']={}
    def add_facility(self,u,v,n,ident,R):
        if not self.G.has_edge(u,v,n):
            return
        self.G.edges[u,v,n]['Facilities'].append(Facility(ident,R))
        self.G.edges[u,v,n]['Facilities'].sort(key=lambda x: x.R, reverse=True)
             
        if len(self.G.edges[u,v,n]['Facilities'])==1:
            self.preprocessR(u,v,n)
        if R<self.G.edges[u,v,n]['Facilities'][0].R:
            return    
        self.preprocess(u,v,n)    
    
    #def get_key(obj):
    #    return obj.R
    def modify(self,ide,u,v,n,newR):
        facility=self.G.edges[u,v,n]['Facilities']
        Rad=-1
        for i in facility:        
            if i.ident==ide:
                Rad=facility[0].R
                i.R=newR
                break
        facility.sort(key=lambda x:x.R,reverse=True) 
        newRad=facility[0].R
        if(Rad==-1):
            print("Facility do not exist")
            return
        if newRad>Rad:
            self.preprocess(u,v,n)
        elif newRad<Rad:
            self.preprocessd(newRad,Rad,u,v,n)
            
    def preprocessd(self,Lbound,Ubound,u,v,n):
        RTD=0
        for w in self.paths[v]:
            for z in self.G.adj[w]:
                for n1 in self.G.adj[w][z]:
                    RTD=self.G.edges[w,z,n1]['length']+self.G.edges[u,v,n]['length']+self.paths[v][w]
                    if u in self.paths[z].keys():
                        RTD+=self.paths[z][u]
                        if RTD>Lbound and RTD<=Ubound:
                            del self.G.edges[w,z,n1]['relevant'][(u,v,n)]
                            self.G.edges[w,z,n1]['relevantR'].update({(u,v,n):RTD})
    def delete_facility(self,u,v,n,ide):
        facility=self.G.edges[u,v,n]['Facilities']
        Rad=facility[0].R
        for i in facility:
            if i.ident==ide:
                if len(facility)==1:
                    self.preprocessd(0,facility[0].R,u,v,n)
                    self.preprocessRDel(u,v,n)
                    facility.clear()
                else:
                    facility.remove(i)
                    facility.sort(key= lambda x:x.R,reverse=True)
                    if(Rad>facility[0].R):
                        self.preprocessd(facility[0].R,Rad,u,v,n)    
                break  
        
    def preprocessRDel(self,u,v,n):
        RTD=0
        Re=50000
        for w in self.paths[v]:
            for z in self.G.adj[w]:
                for n1 in self.G.adj[w][z]:
                    RTD=self.G.edges[w,z,n1]['length']+self.G.edges[u,v,n]['length']+self.paths[v][w]
                    if u in self.paths[z].keys():
                        RTD+=self.paths[z][u]
                        if RTD<=Re: 
                            del self.G.edges[w,z,n1]['relevantR'][(u,v,n)]  
    def preprocessR(self,u,v,n):
        RTD=0
        Re=50000
        for w in self.paths[v]:
            for z in self.G.adj[w]:
                for n1 in self.G.adj[w][z]:
                    RTD=self.G.edges[w,z,n1]['length']+self.G.edges[u,v,n]['length']+self.paths[v][w]
                    if u in self.paths[z].keys():
                        RTD+=self.paths[z][u]
                        if RTD<=Re and (u,v,n) not in self.G.edges[w,z,n1]['relevantR'].keys():
                            self.G.edges[w,z,n1]['relevantR'].update({(u,v,n):RTD})
                            
                            
    def preprocess(self,u,v,n):
        RTD=0
        Re=self.G.adj[u][v][n]['Facilities'][0].R
        for w in self.paths[v]:
            for z in self.G.adj[w]:
                for n1 in self.G.adj[w][z]:
                    RTD=self.G.edges[w,z,n1]['length']+self.G.edges[u,v,n]['length']+self.paths[v][w]
                    if u in self.paths[z].keys():
                        RTD+=self.paths[z][u]
                        if RTD<=Re and (u,v,n) not in self.G.edges[w,z,n1]['relevant'].keys():
                            self.G.edges[w,z,n1]['relevant'].update({(u,v,n):RTD})
                            del self.G.edges[w,z,n1]['relevantR'][(u,v,n)]
                            
    
    def query(self,u,v,n):
        facility=[]
        for w,z,n1 in self.G.edges[u,v,n]['relevant'].keys():
            distance= self.G.edges[u,v,n]['relevant'][(w,z,n1)]
            facility.append(((w,z,n1),distance))
        facility.sort(key=lambda x: x[1])
        for i,d in facility:
            for f in self.G.adj[i[0]][i[1]][i[2]]['Facilities']:
                if d>f.R:
                    break
                print(f.R,d)       
        
            
    def queryR(self,u,v,n,Range):
        facility=[]
        for w,z,n1 in self.G.edges[u,v,n]['relevant'].keys():
            distance= self.G.edges[u,v,n]['relevant'][(w,z,n1)]
            if distance>Range:
                continue
            facility.append(((w,z,n1),distance)) 
                            
        for w,z,n1 in self.G.edges[u,v,n]['relevantR'].keys():
            distance= self.G.edges[u,v,n]['relevantR'][(w,z,n1)]
            if distance>Range:
                continue
            facility.append(((w,z,n1),distance))
        
        facility.sort(key=lambda x: x[1])
        for i,d in facility:                                          
            for i in self.G.adj[i[0]][i[1]][i[2]]['Facilities']:            
                print(d) 
         
         
            

