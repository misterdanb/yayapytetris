import pygame
from pygame.locals import *

import random

def draw_element(screen, config, x, y, color):
    triangle_colors = [ color ] * 4

    j = 0

    for i in [ 3, 2, 0, 1 ]:
        color_div = 1.0 - 1.0 / (float(i + 2) + 2.4)
        new_color = (min(int(triangle_colors[i][0] * color_div), 255),
                     min(int(triangle_colors[i][1] * color_div), 255),
                     min(int(triangle_colors[i][2] * color_div), 255))
        triangle_colors[j] = new_color

        j += 1

    x_off = config.get_window_margin()[3]
    x_block_space = config.get_block_pixel_size()[0] + config.get_block_pixel_padding()[0]
    x_block_size = config.get_block_pixel_size()[0]

    y_off = config.get_window_margin()[0]
    y_block_space = config.get_block_pixel_size()[1] + config.get_block_pixel_padding()[1]
    y_block_size = config.get_block_pixel_size()[1]

    x_block = x_off + x * x_block_space
    y_block = y_off + y * y_block_space

    border_indent = 5.0

    tri_1_points = [ (x_block, y_block),
                     (x_block + x_block_size, y_block),
                     (x_block + x_block_size / 2.0, y_block + y_block_size / 2.0) ]
    tri_2_points = [ (x_block + x_block_size, y_block),
                     (x_block + x_block_size, y_block + y_block_size),
                     (x_block + x_block_size / 2.0, y_block + y_block_size / 2.0) ]
    tri_3_points = [ (x_block + x_block_size, y_block + y_block_size),
                     (x_block, y_block + y_block_size),
                     (x_block + x_block_size / 2.0, y_block + y_block_size / 2.0) ]
    tri_4_points = [ (x_block, y_block + y_block_size),
                     (x_block, y_block),
                     (x_block + x_block_size / 2.0, y_block + y_block_size / 2.0) ]

    rect = [ (x_block + x_block_size / border_indent, y_block + y_block_size / border_indent),
             (x_block + x_block_size - x_block_size / border_indent, y_block + y_block_size / border_indent),
             (x_block + x_block_size - x_block_size / border_indent, y_block + y_block_size - y_block_size / border_indent),
             (x_block + x_block_size / border_indent, y_block + y_block_size - y_block_size / border_indent) ]

    pygame.draw.polygon(screen, triangle_colors[0], tri_1_points)
    pygame.draw.polygon(screen, triangle_colors[1], tri_2_points)
    pygame.draw.polygon(screen, triangle_colors[2], tri_3_points)
    pygame.draw.polygon(screen, triangle_colors[3], tri_4_points)
    pygame.draw.polygon(screen, color, rect)

