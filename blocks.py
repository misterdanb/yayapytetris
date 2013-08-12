import pygame
from pygame.locals import *

import random

class GameBlock(object):
    def __init__(self, config, position, size, mask, color=(255, 255, 255), start_block=0):
        self.config = config
        
        self.position = position
        self.size = size
        
        self.mask = mask
        self.color = color
        
        self.current_block = start_block % 4
    
    def check_for_collision(self, game_field, position=None, block=None):
        if block == None: block = self.current_block
        if position == None: position = self.position
        
        collision = False
        
        for x in range(position[0], position[0] + self.size[0]):
            for y in range(position[1], position[1] + self.size[1]):
                if self.mask[block % 4][x - position[0]][y - position[1]] == 1:
                    if x < 0 or \
                       y < 0 or \
                       x >= self.config.get_field_size()[0] or \
                       y >= self.config.get_field_size()[1]:
                        collision = True
                    elif game_field.get_mask()[x][y] == 1:
                        collision = True
        
        return collision
    
    def rotate(self, game_field, discrete_angle):
        collision = True
        
        if not self.check_for_collision(game_field, self.position, (self.current_block + 4 - discrete_angle % 4) % 4):
            self.current_block = (self.current_block + 4 - discrete_angle % 4) % 4
            collision = False
        
        return collision
    
    def rotate_left(self, game_field):
        return self.rotate(game_field, 1)
    
    def rotate_right(self, game_field):
        return self.rotate(game_field, -1)
    
    def move(self, game_field, way):
        collision = True
        
        if not self.check_for_collision(game_field, (self.position[0] + way[0], self.position[1] + way[1]), self.current_block):
            self.position = (self.position[0] + way[0], self.position[1] + way[1])
            collision = False
        
        return collision
    
    def move_up(self, game_field):
        return self.move(game_field, (0, -1))
    
    def move_down(self, game_field):
        return self.move(game_field, (0, 1))
    
    def move_left(self, game_field):
        return self.move(game_field, (-1, 0))
    
    def move_right(self, game_field):
        return self.move(game_field, (1, 0))
    
    def composite(self, compositing_field):
        for x in range(self.position[0], self.position[0] + self.size[0]):
            for y in range(self.position[1], self.position[1] + self.size[1]):
                if self.mask[self.current_block % 4][x - self.position[0]][y - self.position[1]] == 1:
                    if x >= 0 and \
                       y >= 0 and \
                       x < self.config.get_field_size()[0] and \
                       y < self.config.get_field_size()[1]:
                        compositing_field[x][y] = self.color
    
    def get_position(self):
        return self.position
    
    def get_size(self):
        return self.size
    
    def get_mask(self):
        return self.mask[self.current_block % 4]
    
    def get_color(self):
        return self.color

class I(GameBlock):
    def __init__(self, config, position=(0, 0), color=(255, 255, 255)):
        block_0 = [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]
        block_1 = [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]
        block_2 = [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]
        block_3 = [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]
        
        super(I, self).__init__(config, position, (4, 4), (block_0, block_1, block_2, block_3), color)

class WrongL(GameBlock):
    def __init__(self, config, position=(0, 0), color=(255, 255, 255)):
        block_0 = [[1, 1, 0], [0, 1, 0], [0, 1, 0]]
        block_1 = [[0, 0, 0], [1, 1, 1], [1, 0, 0]]
        block_2 = [[0, 1, 0], [0, 1, 0], [0, 1, 1]]
        block_3 = [[0, 0, 1], [1, 1, 1], [0, 0, 0]]
        
        super(WrongL, self).__init__(config, position, (3, 3), (block_0, block_1, block_2, block_3), color)

class L(GameBlock):
    def __init__(self, config, position=(0, 0), color=(255, 255, 255)):
        block_0 = [[0, 1, 0], [0, 1, 0], [1, 1, 0]]
        block_1 = [[0, 0, 0], [1, 1, 1], [0, 0, 1]]
        block_2 = [[0, 1, 1], [0, 1, 0], [0, 1, 0]]
        block_3 = [[1, 0, 0], [1, 1, 1], [0, 0, 0]]
        
        super(L, self).__init__(config, position, (3, 3), (block_0, block_1, block_2, block_3), color)

class O(GameBlock):
    def __init__(self, config, position=(0, 0), color=(255, 255, 255)):
        block_0 = [[1,1], [1,1]]
        block_1 = [[1,1], [1,1]]
        block_2 = [[1,1], [1,1]]
        block_3 = [[1,1], [1,1]]
        
        super(O, self).__init__(config, position, (2, 2), (block_0, block_1, block_2, block_3), color)

class WrongN(GameBlock):
    def __init__(self, config, position=(0, 0), color=(255, 255, 255)):
        block_0 = [[0, 1, 0], [1, 1, 0], [1, 0, 0]]
        block_1 = [[0, 0, 0], [1, 1, 0], [0, 1, 1]]
        block_2 = [[0, 0, 1], [0, 1, 1], [0, 1, 0]]
        block_3 = [[1, 1, 0], [0, 1, 1], [0, 0, 0]]
        
        super(WrongN, self).__init__(config, position, (3, 3), (block_0, block_1, block_2, block_3), color)

class T(GameBlock):
    def __init__(self, config, position=(0, 0), color=(255, 255, 255)):
        block_0 = [[0, 1, 0], [1, 1, 0], [0, 1, 0]]
        block_1 = [[0, 0, 0], [1, 1, 1], [0, 1, 0]]
        block_2 = [[0, 1, 0], [0, 1, 1], [0, 1, 0]]
        block_3 = [[0, 1, 0], [1, 1, 1], [0, 0, 0]]
        
        super(T, self).__init__(config, position, (3, 3), (block_0, block_1, block_2, block_3), color)

class N(GameBlock):
    def __init__(self, config, position=(0, 0), color=(255, 255, 255)):
        block_0 = [[1, 0, 0], [1, 1, 0], [0, 1, 0]]
        block_1 = [[0, 0, 0], [0, 1, 1], [1, 1, 0]]
        block_2 = [[0, 1, 0], [0, 1, 1], [0, 0, 1]]
        block_3 = [[0, 1, 1], [1, 1, 0], [0, 0, 0]]
        
        super(N, self).__init__(config, position, (3, 3), (block_0, block_1, block_2, block_3), color)
