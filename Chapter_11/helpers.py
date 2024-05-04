import pygame
from random import randint
from typing import *
# HELPERS / SETTINGS

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

width, height = 400, 400

screenshot_mode = False

def to_pixels(x,y):
    mapped_x = width / 2 + (x * width/ 20)
    mapped_y = height / 2 + (y * height/ 20)
    return (mapped_x, mapped_y)

def draw_poly(screen, polygon_model, color=GREEN, fill=False):
    pixel_points = [to_pixels(x,y) for x,y in polygon_model.transformed()]
    if fill:
        pygame.draw.polygon(screen, color, pixel_points, 0)
    else:
        pygame.draw.aalines(screen, color, True, pixel_points, 10)
    if polygon_model.draw_center:
        cx, cy = to_pixels(polygon_model.x, polygon_model.y)
        pygame.draw.circle(screen, color, (int(cx), int(cy)), 4, 4)

def draw_segment(screen, v1,v2,color=RED):
    pygame.draw.aaline(screen, color, to_pixels(*v1), to_pixels(*v2), 10)

def random_x_y(asteroid):
    asteroid.x = randint(-9,9)
    asteroid.y = randint(-9,9)
    return asteroid