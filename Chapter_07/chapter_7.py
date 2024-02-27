from typing import *
from random import randint,uniform
from functools import *
from itertools import *
import pygame 
import vectors
import math

WIDTH = 400 * 2
HEIGHT = 400 * 2
RED = (250, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

class PolygonModel():
    def __init__(self, points: List[float]) -> None:
        self.points = points
        self.rotation_angle = 0
        self.x = 0
        self.y = 0

    def transformed(self):
        rotated = [vectors.rotate2d(self.rotation_angle, v) for v in self.points]
        return [vectors.add((self.x,self.y),v) for v in rotated]

    def move(self, milliseconds):
        dx, dy = self.vx * milliseconds / 1000.0, self.vy * milliseconds / 1000.0
        self.x, self.y = vectors.add((self.x,self.y), (dx,dy))
        self.rotation_angle += self.angular_velocity * milliseconds / 1000.0

class Ship(PolygonModel):
    def __init__(self) -> None:
        super().__init__([(0.5,0), (-0.25,0.25), (-0.25,-0.25)])
    def laser_segment(self):
        dist = 20.0 * math.sqrt(2)
        tip_x,tip_y = self.transformed()[0]
        return ((tip_x, tip_y), (tip_x + dist * math.cos(self.rotation_angle), tip_y + dist * math.sin(self.rotation_angle)))

class Asteroid(PolygonModel):
    def __init__(self) -> None:
        sides = randint(5,9)
        vs = [(vectors.to_cartesian((uniform(0.5, 1.0), math.pi * i * 2 / sides ))) for i in range(sides)]
        super().__init__(vs)

# transforms our representation of pixel to
# pygames representation of a pixel
def to_pixels(x: float, y: float) -> (float, float):
    return (WIDTH/2 + WIDTH * x / 20, HEIGHT/2 - HEIGHT * y / 20)

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
            ship.rotation_angle += milliseconds * (2* math.pi / 1000)

        if keys[pygame.K_RIGHT]:
            ship.rotation_angle -= milliseconds * (2* math.pi / 1000)

        laser = ship.laser_segment()

        # DRAW THE SCENE
        screen.fill(WHITE)

        if keys[pygame.K_SPACE]:
            draw_segment(screen, *laser)

        draw_polygon(screen,ship)

        for asteroid in asteroids:
            # if keys[pygame.K_SPACE] and asteroid.does_intersect(laser):
            #     asteroids.remove(asteroid)
            # else:
            draw_polygon(screen, asteroid, color=GREEN)


        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

