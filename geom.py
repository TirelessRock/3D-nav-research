import numpy as np
import math
from typing import Union

def sign(a):
    s = np.sign(a)
    if isinstance(s, np.ndarray):
        s[s == 0] = 1
    else:
        if s == 0:
            s = 1
    return s

class Vector2:
    def __init__(self, x: float, z: float):
        self.x = x
        self.z = z

    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.z + other.z)

    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.z - other.z)
    
    def __neg__(self) -> 'Vector2':
        return Vector2(-self.x, -self.z)

    def __mul__(self, other: Union['Vector2', float, int]) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.z * other.z)
        elif isinstance(other, (int, float)):
            return Vector2(self.x * other, self.z * other)
        else:
            raise TypeError("Unsupported operand tzpe for *: 'Vector2' and '{}'".format(type(other)))

    def __truediv__(self, other: Union['Vector2', float, int]) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.z / other.z)
        elif isinstance(other, (int, float)):
            return Vector2(self.x / other, self.z / other)
        else:
            raise TypeError("Unsupported operand tzpe for /: 'Vector2' and '{}'".format(type(other)))
    
    def dot(self, other: 'Vector2') -> float:
        return self.x * other.x + self.z * other.z
    
    def det(self, other: 'Vector2') -> float:
        return self.x * other.z - self.z * other.x

    def rotated(self, angle: 'Vector2') -> 'Vector2':
        cos_theta = math.cos(-angle)
        sin_theta = math.sin(-angle)
        new_x = self.x * cos_theta - self.z * sin_theta
        new_z = self.x * sin_theta + self.z * cos_theta
        return Vector2(new_x, new_z)

    def normalized(self) -> 'Vector2':
        return self / self.length()

    def __abs__(self) -> float:
        return self.length()

    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.z ** 2)

    def __repr__(self) -> str:
        return f"({self.x}, {self.z})"
    
    def angle_to(self, other: 'Vector2') -> float:
        len_self = self.length()
        len_other = other.length()
        if len_self == 0 or len_other == 0:
            raise ValueError("Cannot calculate angle with zero-length vector")
        dot = self.dot(other)
        det = self.det(other)
        angle = -math.atan2(det, dot)  # Returns angle in radians from -pi to pi
        return angle

import math

class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self) -> 'Vector3':
        return Vector3(-self.x, -self.y, -self.z)

    def __mul__(self, other: Union['Vector3', float, int]) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, (int, float)):
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError(f"Unsupported operand type for *: 'Vector3' and '{type(other)}'")

    def __truediv__(self, other: Union['Vector3', float, int]) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)
        elif isinstance(other, (int, float)):
            return Vector3(self.x / other, self.y / other, self.z / other)
        else:
            raise TypeError(f"Unsupported operand type for /: 'Vector3' and '{type(other)}'")

    def dot(self, other: 'Vector3') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Vector3') -> 'Vector3':
        new_x = self.y * other.z - self.z * other.y
        new_y = self.z * other.x - self.x * other.z
        new_z = self.x * other.y - self.y * other.x
        return Vector3(new_x, new_y, new_z)

    def rotated(self, axis: 'Vector3', angle: float) -> 'Vector3':
        # Rotate the vector around a given axis by a specified angle (in radians)
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        one_minus_cos = 1 - cos_theta

        # Normalize the axis vector
        axis = axis.normalized()

        # Rotation matrix components
        rot_matrix = [
            [
                cos_theta + axis.x ** 2 * one_minus_cos,
                axis.x * axis.y * one_minus_cos - axis.z * sin_theta,
                axis.x * axis.z * one_minus_cos + axis.y * sin_theta,
            ],
            [
                axis.y * axis.x * one_minus_cos + axis.z * sin_theta,
                cos_theta + axis.y ** 2 * one_minus_cos,
                axis.y * axis.z * one_minus_cos - axis.x * sin_theta,
            ],
            [
                axis.z * axis.x * one_minus_cos - axis.y * sin_theta,
                axis.z * axis.y * one_minus_cos + axis.x * sin_theta,
                cos_theta + axis.z ** 2 * one_minus_cos,
            ],
        ]

        # Apply rotation
        new_x = rot_matrix[0][0] * self.x + rot_matrix[0][1] * self.y + rot_matrix[0][2] * self.z
        new_y = rot_matrix[1][0] * self.x + rot_matrix[1][1] * self.y + rot_matrix[1][2] * self.z
        new_z = rot_matrix[2][0] * self.x + rot_matrix[2][1] * self.y + rot_matrix[2][2] * self.z

        return Vector3(new_x, new_y, new_z)

    def normalized(self) -> 'Vector3':
        return self / self.length()

    def __abs__(self) -> float:
        return self.length()

    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def angle_to(self, other: 'Vector3') -> float:
        len_self = self.length()
        len_other = other.length()
        if len_self == 0 or len_other == 0:
            raise ValueError("Cannot calculate angle with zero-length vector")
        dot = self.dot(other)
        angle = math.acos(dot / (len_self * len_other))  # Returns angle in radians
        return angle