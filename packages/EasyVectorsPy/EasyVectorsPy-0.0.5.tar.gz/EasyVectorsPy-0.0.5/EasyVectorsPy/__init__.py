from math import hypot
class Vector2:

    __slots__ = ('__x', '__y')


    def __init__(self, x=0, y=0):
        self.__x = x
        self.__y = y 

    def __str__(self):
        return f'X {self.__x} Y {self.__y}'
    
    @property
    def x(self):
        return self.__x
    
    @x.setter
    def x(self, num):
        self.__x += num

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, num):
        self.__y += num
    
    def zero(self):
        self.__x, self.__y = 0, 0
    
    def update(self, x=0,y=0):
        self.__x += Vector2.__isint(x)
        self.__y += Vector2.__isint(y)


    @staticmethod
    def __isint(value):
        if isinstance(value, int):
            return value 
        else:
            raise TypeError("Must be int", value)

    
    def distance_to(self, vector):
        if not isinstance(vector, Vector2):
            raise ValueError("Must be Vector2")
        else:
            return hypot(self.__x - vector.__x, self.__y - vector.__y)

    

