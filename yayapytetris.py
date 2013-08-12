import pygame
from pygame.locals import *

import random
import time
import telnetlib

import config
import field
import blocks

class Game(object):
    def __init__(self, config):
        self.config = config
        
        self.screen = None
        self.running = False
        
        self.game_field = field.GameField(config)
        
        self.current_block = None
        self.fall_speed = self.config.get_automatic_fall_start_speed()
        self.fall_field_counter = 0
        self.fall_speed_up_counter = 0
        
        if self.config.get_display_type() == "blinkdevice":
            self.china_telnet = telnetlib.Telnet()
            
            try:
                self.china_telnet.open("localhost")
            except:
                pass
        
            self.china_counter = 0
        
    def start(self):
        pygame.init()
        
        if self.config.get_display_type() == "pygame":
            self.screen = pygame.display.set_mode((self.config.get_field_size()[0] * (self.config.get_block_pixel_size()[0] +
                                                                                      self.config.get_block_pixel_padding()[0]) +
                                                   self.config.get_window_margin()[3] +
                                                   self.config.get_window_margin()[1],
                                                   self.config.get_field_size()[1] * (self.config.get_block_pixel_size()[1] +
                                                                                      self.config.get_block_pixel_padding()[1]) +
                                                   self.config.get_window_margin()[0] +
                                                   self.config.get_window_margin()[2]))
        elif self.config.get_display_type() == "blinkdevice":
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        pygame.display.set_caption("Yayapytetris, here we go!")
        pygame.display.update()
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(1, 100)
        
        self.game_loop()
        
    def game_loop(self):
        self.running = True
        
        self.generate_new_block()
        
        loop_begin_time = pygame.time.get_ticks()
        
        while self.running:
            delta_time = pygame.time.get_ticks() - loop_begin_time
            loop_begin_time = pygame.time.get_ticks()
            
            self.process_inputs()
            self.process_game_logic(delta_time)
            self.process_graphics()
            self.process_sounds(delta_time)
    
    def process_inputs(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
                elif event.key == K_LEFT:
                    self.current_block.move_left(self.game_field)
                elif event.key == K_RIGHT:
                    self.current_block.move_right(self.game_field)
                elif event.key == K_UP:
                    # hahaha... no.jpg
                    #self.current_block.move_up(self.game_field)
                    pass
                elif event.key == K_DOWN:
                    if self.current_block.check_for_collision(self.game_field,
                                                             (self.current_block.get_position()[0],
                                                              self.current_block.get_position()[1] + 1)):
                        self.game_field.merge_block(self.current_block)
                        self.generate_new_block()
                        
                        if self.current_block.check_for_collision(self.game_field, self.current_block.get_position()):
                            pygame.event.post(pygame.event.Event(QUIT))
                    else:
                        self.current_block.move_down(self.game_field)
                elif event.key == K_COMMA:
                    self.current_block.rotate_left(self.game_field)
                elif event.key == K_PERIOD:
                    self.current_block.rotate_right(self.game_field)
    
    def process_game_logic(self, delta_time):
        self.fall_field_counter += self.fall_speed * delta_time
        self.fall_speed_up_counter += delta_time
        
        if self.config.get_display_type() == "blinkdevice":
            self.china_counter += delta_time
        
        if self.fall_speed_up_counter > self.config.get_automatic_fall_speed_up_time_step():
            self.fall_speed_up_counter %= self.config.get_automatic_fall_speed_up_time_step()
            self.fall_speed += self.config.get_automatic_fall_speed_up_step()
        
        if self.fall_field_counter > 1:
            self.fall_field_counter %= 1
            
            if self.current_block.check_for_collision(self.game_field,
                                                      (self.current_block.get_position()[0],
                                                       self.current_block.get_position()[1] + 1)):
                self.game_field.merge_block(self.current_block)
                self.generate_new_block()
                
                if self.current_block.check_for_collision(self.game_field, self.current_block.get_position()):
                    pygame.event.post(pygame.event.Event(QUIT))
            else:
                self.current_block.move_down(self.game_field)
        
        self.game_field.remove_full_lines()
    
    def process_graphics(self):
        compositing_field = [[(80, 80, 80)] * self.config.get_field_size()[1] for n in range(self.config.get_field_size()[0])]
        
        self.game_field.composite(compositing_field)
        self.current_block.composite(compositing_field)
        
        if self.config.get_display_type() == "pygame":
            for x in range(self.config.get_field_size()[0]):
                for y in range(self.config.get_field_size()[1]):                    
                    if self.config.get_tilt_screen():
                        block_rectangle = (self.config.get_window_margin()[0] + (self.config.get_block_pixel_size()[1] + self.config.get_block_pixel_padding()[1]) * y,
                                           self.config.get_window_margin()[3] + (self.config.get_block_pixel_size()[0] + self.config.get_block_pixel_padding()[0]) * (self.get_field_size()[0] - 1 - x),
                                           self.config.get_block_pixel_size()[1],
                                           self.config.get_block_pixel_size()[0])
                    else:
                        block_rectangle = (self.config.get_window_margin()[3] + (self.config.get_block_pixel_size()[0] + self.config.get_block_pixel_padding()[0]) * x,
                                           self.config.get_window_margin()[0] + (self.config.get_block_pixel_size()[1] + self.config.get_block_pixel_padding()[1]) * y,
                                           self.config.get_block_pixel_size()[0],
                                           self.config.get_block_pixel_size()[1])
                    
                    pygame.draw.rect(self.screen,
                                     pygame.color.Color(compositing_field[x][y][0],
                                                        compositing_field[x][y][1],
                                                        compositing_field[x][y][2],
                                                        255),
                                     block_rectangle)
                    
            pygame.display.flip()
        elif self.config.get_display_type() == "blinkdevice":
            if self.china_counter > 50:
                self.china_counter %= 50
                
                blinkode = ""
                
                for x in range(self.config.get_field_size()[0]):
                    for y in range(self.config.get_field_size()[1]):
                        if self.config.get_tilt_screen():
                            blinkode += "sp" + \
                                        str(y) + "," + \
                                        str(self.config.get_field_size()[0] - 1 - x) + "," + \
                                        str(compositing_field[x][y][0] / 255.0) + "," + \
                                        str(compositing_field[x][y][1] / 255.0) + "," + \
                                        str(compositing_field[x][y][2] / 255.0) + ";"
                        else:
                            blinkode += "sp" + \
                                        str(x) + "," + \
                                        str(y) + "," + \
                                        str(compositing_field[x][y][0] / 255.0) + "," + \
                                        str(compositing_field[x][y][1] / 255.0) + "," + \
                                        str(compositing_field[x][y][2] / 255.0) + ";"
                
                blinkode += "ac;"
                
                self.china_telnet.write(blinkode)

    def process_sounds(self, delta_time):
        pass
    
    def generate_new_block(self):
        approximated_half_block_length = 1
        all_blocks = [blocks.I, blocks.WrongL, blocks.L, blocks.O, blocks.WrongN, blocks.T, blocks.N]
        self.current_block = all_blocks[random.randint(0, 6)](self.config,
                                                              (self.config.get_field_size()[0] / 2 - approximated_half_block_length, 0),
                                                              (random.randint(130, 255),
                                                               random.randint(130, 255),
                                                               random.randint(130, 255))) 
