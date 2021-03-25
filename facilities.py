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
