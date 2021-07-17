import random
class Facility:  
    def __init__(self,ident, R, length=0, d = 0, max_rad = 200):
        self.ident = ident
        self.R = R 
        self.d = d if d != 0 else random.uniform(0, 1)
        self.d = self.d * length
        self.max_rad = max_rad
        self.length = length
        
    def invert(self):
        self.d = self.length - self.d
        return self
    
    def __str__(self):
        return f'\nid = {self.ident}, R = {self.R}'
    
    def __repr__(self):
        return self.__str__()
    