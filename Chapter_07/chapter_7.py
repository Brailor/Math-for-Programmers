from typing import *
from random import randint,uniform
from functools import *
from itertools import *
import pygame 
import vectors
import math
import lineq
import draw2d

WIDTH = 400
HEIGHT = 400
RED = (250, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Exercise 7.1: Implement a transformed() method on the PolygonModel that returns the points of the model translated by
# the object’s x and y attributes and rotated by its rotation_angle attribute.
class PolygonModel():
    def __init__(self, points: List[float]) -> None:
        self.points = points
        self.rotation_angle = 0
        self.x = 0
        self.y = 0
    # Exercise 7.14: Write a does_collide(other_polygon) method to decide whether the current PolygonModel
    # object collides with another other_polygon by checking whether any of the segments that define the two are intersecting.
    # This could help us decide whether an asteroid has hit the ship or another asteroid.
    def does_collide(self, other_polygon: Type[Self]):
        # how to do this?
        # 1st. idea: go through each segment of poly a, and check wheter it intersects with any segment of poly b
        for other_segment in other_polygon.segments():
            if self.does_segment_intersect(other_segment):
                    return True
        return False
    
    def transformed(self):
        ps = [vectors.rotate2d(self.rotation_angle, vec) for vec in self.points]
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

    def does_intersect(self, other_segment) -> bool:
        return super().does_segment_intersect(other_segment) 

# Exercise 7.2: Write a function to_pixels(x,y) that takes a pair of x − and y-coordinates in the square where −10 < x < 10 and −10 < y < 10
# and maps them to the corresponding PyGame x and y pixel coordinates, each ranging from 0 to 400.
# transforms our representation of pixel to
# pygames representation of a pixel
def to_pixels(x,y):
    mapped_x = WIDTH / 2 + (x * WIDTH / 20)
    mapped_y = HEIGHT / 2 + (y * HEIGHT / 20)
    return (mapped_x, mapped_y)


def draw_polygon(screen, polygon_model, color = GREEN):
    pixel_points = [to_pixels(x, y) for (x,y) in polygon_model.transformed()]
    pygame.draw.aalines(screen, color, True, pixel_points, 10)

def draw_segment(screen, v1,v2,color=RED):
    pygame.draw.aaline(screen, color, to_pixels(*v1), to_pixels(*v2), 10)

ship = Ship()

def random_x_y(asteroid: Asteroid) -> Asteroid:
    asteroid.x = randint(-9,9)
    asteroid.y = randint(-9,9)
    return asteroid
asteroid_count = 10
asteroids = list(map(random_x_y, [Asteroid() for _ in range(asteroid_count)]))
print(f"Ship: {ship}, asteroids: {asteroids}")

def main():
    pygame.init()

    screen = pygame.display.set_mode([WIDTH,HEIGHT])
    
    pygame.display.set_caption("Asteroids!")

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
            pass
            # ast.move(milliseconds)

        if keys[pygame.K_LEFT]:
            ship.rotation_angle -= milliseconds * (2* math.pi / 1000)

        if keys[pygame.K_RIGHT]:
            ship.rotation_angle += milliseconds * (2* math.pi / 1000)

        laser = ship.laser_segment()

        # DRAW THE SCENE
        screen.fill(WHITE)

        if keys[pygame.K_SPACE]:
            draw_segment(screen, *laser)

        draw_polygon(screen,ship)

        for asteroid in asteroids:
            if keys[pygame.K_SPACE] and asteroid.does_intersect(laser):
                asteroids.remove(asteroid)
            else:
                draw_polygon(screen, asteroid, color=GREEN)


        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()


# Exercise 7.13: For the example laser line and asteroid, confirm the does_intersect function returns True
# (Hint: use grid lines to find the vertices of the asteroid and build a PolygonModel object representing it.)
asteroid = [(2, 7), (1, 5), (2, 3), (4, 2), (6, 2), (7, 4), (6, 6),(4, 6)]
laser = [(1,1), (7,7)]
ast = Asteroid(asteroid)
print(ast.does_segment_intersect(laser))
# print(f"Lasert: {laser}")
# for segment in ast.segments():
#     print(f"Segment: {segment}")
#     print(f"Does intersect with laser? => {lineq.segment_check(segment, laser)}")
# draw2d.draw2d(draw2d.Polygon2D(*ast.points), draw2d.Segment2D(laser[0], laser[1], color='C3'))

p1 = PolygonModel(asteroid)
p2 = PolygonModel([(4,1), (5,3), (6,1)])
p3 = PolygonModel([(4,-1), (4,1), (5,1), (5,-1)])
print(p1.does_collide(p2))
print(p2.does_collide(p3))
print(p1.does_collide(p3))
draw2d.draw2d(
    draw2d.Polygon2D(*p1.points),
    draw2d.Polygon2D(*p2.points),
    draw2d.Polygon2D(*p3.points),
)

