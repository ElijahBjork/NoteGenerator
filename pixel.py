"""
Author:  Elijah Bjork
Purpose: Defines a pixel class
"""

class pixel(dict):

    
    def __init__(self, pt, rgb):
        self.x = pt[0] 
        self.y = pt[1] 
        self.r = rgb[0] 
        self.g = rgb[1] 
        self.b = rgb[2]
        hex_r = hex(self.r)
        hex_g = hex(self.g)
        hex_b = hex(self.b)
        self.hex = '#{}{}{}'.format(hex_r[2:].zfill(2), hex_g[2:].zfill(2), hex_b[2:].zfill(2))
        dict.__init__(self, x = pt[0] , y = pt[1] , r = rgb[0] , g = rgb[1] , b = rgb[2], hex = self.hex)

    def get_pt(self):
        return (self.x, self.y)
    
    def get_rgb(self):
        return [self.r, self.g, self.b]
    
    def get_hex(self):
        return self.hex
    
    def __str__(self):
        return "{ 'x': " + str(self.x).zfill(4) + ", 'y': " + str(self.y).zfill(4) +", 'r': " + str(self.r).zfill(3) + ", 'g': " + str(self.g).zfill(3) + ", 'b': " + str(self.b).zfill(3) +" } "

    