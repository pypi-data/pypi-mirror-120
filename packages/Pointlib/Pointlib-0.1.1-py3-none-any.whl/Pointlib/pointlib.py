class Point:

    def __init__(self, x:float = 0.0, y:float = 0.0, z:float = 0.0):

        self.coor = (x, y, z)
        self.x = x
        self.y = y
        self.z = z
        
    def to2D(self):
        return (self.x, self.y)
    
    def to3D(self):
        return (self.x, self.y, self.z)
    
    def get_x(self): 
        return self.x

    def get_y(self): 
        return self.y

    def get_z(self): 
        return self.z

    def neg_x(self): 
        return -(self.x)

    def neg_y(self): 
        return -(self.y)

    def neg_z(self): 
        return -(self.z)

    def slope_from_origin(self):
        if self.x == 0:
            return float('inf')
        else:
            return self.y / self.x

def distance(point1:Point, point2:Point):
    return (( ((point1.x - point2.x)**2) + ((point1.y - point2.y)**2) + ((point1.z - point2.z)**2) )**0.5)

def slove2D(point1:Point, point2:Point):
    return (point2.y - point1.y) / (point2.x - point1.x) if (point2.x - point1.x)!=0 else float('inf')

def halfway2D(point1:Point, point2:Point):
    return Point(((point1.x + point2.x) / 2.0), (point1.y + point2.y) / 2.0)
