from geom import sign, Vector2, Vector3

from math import sqrt, atan2, cos, sin
import numpy as np
from numpy import deg2rad, rad2deg
from typing import Optional
from enum import Enum

def clamp(value: float, minvalue: float, maxvalue: float) -> float:
    return max(minvalue, min(maxvalue, value))

def rotate_towards_vector(origin: Vector2, dest: Vector2, angle: float) -> Vector2:
    if (origin == dest):
        return origin
    
    if (origin.angle_to(dest) < 0):
        angle *= -1
    return origin.rotated(angle)

class MoveSet(Enum):
    FREE = 0
    CIRCLE = 1
    ROTATE = 2
    DAMP = 3

class Ship:
    def __init__(self):

        self.pos = Vector2(0, 0)
        self.tilt = Vector2(0, 0)
        self.delta_controlled = float(0.0)

        self.direction = Vector2(0, 1)
        self.next_wp = Vector2(20, 20)
        self.movement_direction = Vector2(0, 1)
        
        self.speed = 5.0
        self.maxspeed = 30.0

        self.omega = 0
        self.omega_max = 0.9
        self.eps = 0

        self.handleability = 4
        self.max_tilt = 0.4

        self.max_yaw_speed = self.max_pitch_speed = deg2rad(90)
        self.angular_mobility = 2.0
    
    def copy(self) -> 'Ship':
        s = Ship()

        s.pos = self.pos
        s.tilt = self.tilt
        s.delta_controlled = self.delta_controlled

        s.direction = self.direction
        s.next_wp = self.next_wp
        s.movement_direction = self.movement_direction
        
        s.speed = self.speed
        s.maxspeed = self.maxspeed

        s.omega = self.omega
        s.omega_max = self.omega_max
        s.eps = self.eps

        s.handleability = self.handleability
        s.max_tilt = self.max_tilt

        s.max_yaw_speed = self.max_yaw_speed
        s.max_pitch_speed = self.max_pitch_speed
        s.angular_mobility = self.angular_mobility

        return s
    
    def set_next_wp(self, nwp: Vector2):
        self.next_wp = nwp
    
    def get_theta(self):
        return self.direction.angle_to(self.next_wp - self.pos)

    def to_local(self, target):
        target_rel = target - self.pos
        angle = self.direction.angle_to(target_rel)
        return Vector2(0, 1).rotated(angle)

    def to_global(self, target_rel):
        angle = Vector2(0, 1).angle_to(target_rel)
        return self.pos + self.direction.rotated(angle)

    def current_max_tilt(self) -> float:
        return self.max_tilt * self.handleability / sqrt(self.speed)
    
    def apply_tilt_with_boundaries(self, delta: float, delta_controlled: float) -> float:
        yaw = clamp(delta_controlled, -self.max_yaw_speed, self.max_yaw_speed)
        yaw *= delta
        tilt = clamp(self.tilt.x + yaw, -self.current_max_tilt(), self.current_max_tilt())
        diff = tilt - self.tilt.x
        self.tilt.x = tilt
        return diff
    
    def apply_yaw(self, yaw_angle: float):
        self.rotate_local(yaw_angle)

    def rotate_local(self, angle: float):
        self.direction = self.direction.rotated(angle)
    
    def get_speed_tilt(self, tilt: Vector2) -> float:
        return clamp(tilt.x * self.angular_mobility, -self.omega_max, self.omega_max)

    def rotate_movement(self, tilt: float):
        self.movement_direction = rotate_towards_vector(self.movement_direction, self.direction, tilt)
        self.tilt.x -= tilt

    def update_orientation(self):
        # godot 3d internal
        pass

    # assuming moveset is FREE or <tilt> and <speed> were adjusted beforehand
    def move(self, delta: float, verbose=False, verboselvl=0):
        self.speed = clamp(self.speed, 0, self.maxspeed)

        delta_angles = self.apply_tilt_with_boundaries(delta, self.delta_controlled)
        self.apply_yaw(delta_angles)

        movement_tilt = self.get_speed_tilt(self.tilt)
        movement_tilt *= delta
        if verbose:
            if verboselvl >= 2:
                # print('desired rotation', self.delta_controlled)
                print('bounded rotation', delta_angles)
                print('rotate by', movement_tilt)
                print(
                    '%.2e, %.2e' % (
                        Vector2(0, 1).angle_to(self.direction),
                        self.movement_direction.angle_to(self.direction)
                    ),
                    self.tilt
                )
            if verboselvl >= 1:
                print(f"p: {self.pos:.3f}, tilt: {self.tilt:.3f}")

        self.delta_controlled = 0.0
        self.rotate_movement(movement_tilt)
        self.update_orientation()

        self.pos += self.movement_direction * self.speed * delta
        return self.pos, self.get_theta()
    
    def move_smart(self, delta: float, moveset: MoveSet, verbose=False, verboselvl=0):
        if verbose and verboselvl >= 2:
            print('\n', moveset, self.eps)

        if moveset == MoveSet.FREE:
            self.delta_controlled = 0
        elif moveset == MoveSet.CIRCLE:
            self.delta_controlled = 0
            self.tilt = Vector2(self.omega / self.angular_mobility, 0)
            self.direction = self.movement_direction.rotated(self.omega / self.angular_mobility)
        elif moveset == MoveSet.ROTATE:
            self.delta_controlled = self.eps / self.angular_mobility
        elif moveset == MoveSet.DAMP:
            pass

        return self.move(delta, verbose, verboselvl)