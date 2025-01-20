import numpy as np
import math

def sign(a):
    s = np.sign(a)
    if isinstance(s, np.ndarray):
        s[s == 0] = 1
    else:
        if s == 0:
            s = 1
    return s
class Vector2:
    def __init__(self, x, z):
        self.x = x
        self.z = z

    def __add__(self, other):
        return Vector2(self.x + other.x, self.z + other.z)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.z * other.z)
        elif isinstance(other, (int, float)):
            return Vector2(self.x * other, self.z * other)
        else:
            raise TypeError("Unsupported operand tzpe for *: 'Vector2' and '{}'".format(type(other)))
    
    def dot(self, other):
        return self.x * other.x + self.z * other.z
    
    def det(self, other):
        return self.x * other.z - self.z * other.x

    def rotated(self, angle):
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        new_x = self.x * cos_theta - self.z * sin_theta
        new_z = self.x * sin_theta + self.z * cos_theta
        return Vector2(new_x, new_z)

    def normalized(self):
        return self / self.length()

    def __abs__(self):
        return self.length()

    def length(self):
        return math.sqrt(self.x ** 2 + self.z ** 2)

    def __repr__(self):
        return f"({self.x}, {self.z})"
    
    def angle_to(self, other):
        len_self = self.length()
        len_other = other.length()
        if len_self == 0 or len_other == 0:
            raise ValueError("Cannot calculate angle with zero-length vector")
        dot = self.dot(other)
        det = self.det(other)
        angle = math.atan2(det, dot)  # Returns angle in radians from -pi to pi
        return angle