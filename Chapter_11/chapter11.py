# Import a library of functions called 'pygame'
import pygame
import vectors
from math import pi, sqrt, cos, sin, atan2
from random import randint, uniform
from linear_solver import do_segments_intersect
from helpers import *

# DEFINE OBJECTS OF THE GAME

from typing import *
from random import randint,uniform
from functools import *
from itertools import *
import pygame 
import vectors
import math
import lineq

WIDTH = 400
HEIGHT = 400
RED = (250, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ACCELERATION = 3
DECLERATION = 1.3

class PolygonModel():
    def __init__(self, points: List[float]) -> None:
        self.points = points
        self.rotation_angle = 0
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.draw_center = False 
        self.graviyt = 0

    def does_collide(self, other_polygon: Type[Self]):
        for other_segment in other_polygon.segments():
            if self.does_segment_intersect(other_segment):
                    return True
        return False
    
    def transformed(self):
        ps = map(lambda vec: vectors.rotate2d(self.rotation_angle, vec), self.points)
        return [(self.x + x, self.y + y) for (x,y) in ps]

    def segments(self):
        point_count = len(self.points)
        points = self.transformed()
        return [(points[i], points[(i+1) % point_count])
                for i in range(0,point_count)]

    def does_segment_intersect(self, other_segment):
        for segment in self.segments():
            if lineq.do_segments_intersect(segment, other_segment):
                return True
        return False
    
    def move(self, milliseconds):
        dx, dy = (self.vx * milliseconds / 1000.0, self.vy * milliseconds / 1000.0)
        next_pos_vector = vectors.add((self.x, self.y), (dx, dy))
        self.x = next_pos_vector[0]
        self.y = next_pos_vector[1]

        if self.x < -10:
            self.x += 20
        if self.y < -10:
            self.y += 20
        if self.x > 10:
            self.x -= 20
        if self.y > 10:
            self.y -= 20


class Ship(PolygonModel):
    def __init__(self) -> None:
        super().__init__([(0.5,0), (-0.25,0.25), (-0.25,-0.25)])
    def laser_segment(self):
        dist = 20.0 * math.sqrt(2)
        tip_x,tip_y = self.transformed()[0]
        return ((tip_x, tip_y), (tip_x + dist * math.cos(self.rotation_angle), tip_y + dist * math.sin(self.rotation_angle)))

class Asteroid(PolygonModel):
    def __init__(self, vecs=None) -> None:
        vs = []
        if vecs == None or len(vecs) == 0:
            sides = randint(5,9)
            vs = [(vectors.to_cartesian((uniform(0.5, 1.0), math.pi * i * 2 / sides ))) for i in range(sides)]
        else:
            vs = vecs 
        super().__init__(vs)
        self.vx = uniform(-1, 1)
        self.vy = uniform(-1, 1)

    def does_intersect(self, other_segment) -> bool:
        return super().does_segment_intersect(other_segment) 

class BlackHole(PolygonModel):
    def __init__(self, gravity):
        vs = [vectors.to_cartesian((0.5, 2 * pi * i / 20)) for i in range(0, 20)]
        super().__init__(vs)
        self.gravity = gravity
        self.draw_center = True



ship = Ship()

asteroid_count = 10
asteroids = list(map(random_x_y, [Asteroid() for _ in range(asteroid_count)]))
print(f"Ship: {ship}, asteroids: {asteroids}")

def main():
    pygame.init()

    screen = pygame.display.set_mode([WIDTH,HEIGHT])
    
    pygame.display.set_caption("Asteroids!")
    black_hole = BlackHole(0.1)

    done = False
    clock = pygame.time.Clock()
    while not done:

        clock.tick()

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop

        # UPDATE THE GAME STATE

        milliseconds = clock.get_time()
        keys = pygame.key.get_pressed()

        for ast in asteroids:
            # pass
            ast.move(milliseconds)
        
        if keys[pygame.K_UP]:
            ax = ACCELERATION * math.cos(ship.rotation_angle)
            ay = ACCELERATION * math.sin(ship.rotation_angle)
            ship.vx += ax * milliseconds / 1000.0
            ship.vy += ay * milliseconds / 1000.0

        if keys[pygame.K_DOWN]:
            ax = DECLERATION * math.cos(ship.rotation_angle)
            ay = DECLERATION * math.sin(ship.rotation_angle)
            ship.vx -= ax * milliseconds / 1000.0
            ship.vy -= ay * milliseconds / 1000.0
        
        ship.move(milliseconds)

        if keys[pygame.K_LEFT]:
            ship.rotation_angle -= milliseconds * (2* math.pi / 1000)

        if keys[pygame.K_RIGHT]:
            ship.rotation_angle += milliseconds * (2* math.pi / 1000)

        laser = ship.laser_segment()

        # DRAW THE SCENE
        screen.fill(WHITE)

        if keys[pygame.K_SPACE]:
            draw_segment(screen, *laser)

        draw_poly(screen, ship, color=BLUE)
        draw_poly(screen, black_hole, color=BLACK, fill=True)

        for asteroid in asteroids:
            if keys[pygame.K_SPACE] and asteroid.does_intersect(laser):
                asteroids.remove(asteroid)
            else:
                draw_poly(screen, asteroid,)


        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
