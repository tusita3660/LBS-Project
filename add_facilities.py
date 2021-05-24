from basic_imports import *
from constants import *

def add_facilities(north, south, east, west, pf = 0.5, max_facilities = 15):
    orig = ox.graph_from_bbox(north, south, east, west, network_type='drive')
    H = copy.deepcopy(orig)
    for u, v, n in orig.edges:
        
        if not H.has_edge(u, v, n):
            H.remove_edge(u,v,n)
            continue
        
        l = H.edges[u,v,n]['length']
        oneway = H.edges[u,v,n]['oneway']
        
        if (not oneway) and (not H.has_edge(v,u,n)) :
            while H.has_edge(u,v) or H.has_edge(v,u):
                H.remove_edges_from([(u,v), (v,u)] * 4)
            continue
        
        if 'facilities' not in H.edges[u,v,n].keys():
            
            #load facilities from reverse edge if applicable
            if (not oneway) and ('facilities' in H.edges[v,u,n].keys()):
                H.edges[u,v,n]['facilities'] = [
                            copy.deepcopy(facility).invert() for facility in H.edges[v,u,n]['facilities']]
            
            else:
                H.edges[u,v,n]['facilities'] = []
                if random.choices([0, 1], [1 - pf, pf])[0]:                

                    for i in range(random.randint(1, max_facilities)):
                        H.edges[u,v,n]['facilities'].append(Facility(l))

                    if not oneway:
                        H.edges[v,u,n]['facilities'] = [
                            copy.deepcopy(facility).invert() for facility in H.edges[u,v,n]['facilities']]
                        
                else:
                    H.edges[u,v,n]['facilities'] = []
                    
    H = nx.convert_node_labels_to_integers(H)

    return H
