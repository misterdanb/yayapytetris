import pygame
import elements

class GameField(object):
    def __init__(self, config):
        self.config = config
        
        self.mask = [ [ 0 ] * self.config.get_field_size()[1] for n in range(self.config.get_field_size()[0]) ]
        self.colors = [ [ (0, 0, 0) ] * self.config.get_field_size()[1] for n in range(self.config.get_field_size()[0]) ]
    
    def remove_full_lines(self):
        for i in range(self.config.get_field_size()[1]):
            while sum(self.mask[n][self.config.get_field_size()[1] - 1 - i] for n in range(self.config.get_field_size()[0])) == self.config.get_field_size()[0]:
                for x in range(self.config.get_field_size()[0]):
                    reversed_y = range(1, self.config.get_field_size()[1] - i)
                    reversed_y.reverse()
                    
                    for y in reversed_y:
                        self.mask[x][y] = self.mask[x][y - 1]
                        self.colors[x][y] = self.colors[x][y - 1]
                    
                    self.mask[x][0] = 0
                    self.colors[x][0] = (0, 0, 0)
    
    def merge_block(self, game_block):
        for x in range(game_block.get_position()[0], game_block.get_position()[0] + game_block.get_size()[0]):
            for y in range(game_block.get_position()[1], game_block.get_position()[1] + game_block.get_size()[1]):
                if game_block.get_mask()[x - game_block.get_position()[0]][y - game_block.get_position()[1]] == 1:
                    if x >= 0 and \
                       y >= 0 and \
                       x < self.config.get_field_size()[0] and \
                       y < self.config.get_field_size()[1]:
                        self.mask[x][y] = 1
                        self.colors[x][y] = game_block.get_color()
    
    def composite(self, compositing_field):
        for x in range(self.config.get_field_size()[0]):
            for y in range(self.config.get_field_size()[1]):
                if self.mask[x][y] == 1:
                    if x >= 0 and \
                       y >= 0 and \
                       x < self.config.get_field_size()[0] and \
                       y < self.config.get_field_size()[1]:
                        compositing_field[x][y] = self.colors[x][y]

    def draw(self, screen):
        for x in range(self.config.get_field_size()[0]):
            for y in range(self.config.get_field_size()[1]):
                if self.mask[x][y] == 1:
                    if x >= 0 and \
                       y >= 0 and \
                       x < self.config.get_field_size()[0] and \
                       y < self.config.get_field_size()[1]:
                        elements.draw_element(screen, self.config, x, y, self.colors[x][y])
    
    def get_mask(self):
        return self.mask
    
    def get_colors(self):
        return self.colors
