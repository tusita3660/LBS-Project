class Facility:  
    def __init__(self, length, R = 0, d = 0, max_rad = 200):
        self.R = R if R != 0 else random.randint(1, max_rad)
        self.d = d if d != 0 else random.uniform(0, 1)
        self.d = self.d * length
        self.max_rad = max_rad
        self.length = length
        
    def invert(self):
        self.d = self.length - self.d
        return self
    
    def __str__(self):
        return f'\nR = {self.R}, d = {self.d}, l = {self.length}'
    
    def __repr__(self):
        return self.__str__()
    