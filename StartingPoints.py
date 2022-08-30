"""
Author:  Elijah Bjork
Purpose: Define the StartingPoints Class
"""
from tkinter.messagebox import showinfo

class StartingPoints:
    """Defines a list of starting points"""

    class Point:
        """Defines a point""" 
        def __init__(self, x, y):
            self.x = x
            self.y = y   

        def __str__(self):
            return '(' + str(self.x) + ', ' + str(self.y) + ')'
        
        def asTuple(self):
            return (self.x, self.y)

    def __init__(self):
        self.starting_points = []


    def add_point(self, x, y):
        self.starting_points.append(self.Point(x, y))
        
        
    def remove_point(self, x, y):
        x_points = [point for point in self.starting_points if point.x == x]
        y_points = [point for point in self.starting_points if point.y == y]

        union_intersect = [point for point in x_points if point in y_points]
        
        if len(union_intersect) > 0:
            self.starting_points.remove(union_intersect[0])
        else:
            showinfo(title='Error', message='Point (' + str(x) + ', ' + str(y) + ') doesn\'t exist.')
        