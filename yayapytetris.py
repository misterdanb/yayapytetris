import pygame
from pygame.locals import *
import pyscope
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

import random
import time
import telnetlib

import config
import field
import blocks

class Texture(object):
    def __init__(self, surface=None):
        self.tex_id = glGenTextures(1)
        self.surface = surface

        if surface != None:
            self.update(surface)

    def update(self, surface=None):
        if surface != None and self.surface != surface:
            self.surface = surface

        if self.surface != None:
            try:
                self.tex_data = pygame.image.tostring(self.surface, "RGBA", 1)
                glBindTexture(GL_TEXTURE_2D, self.tex_id)
                glTexImage2D(GL_TEXTURE_2D,
                             0,
                             GL_RGBA,
                             self.surface.get_width(),
                             self.surface.get_height(),
                             0, GL_RGBA,
                             GL_UNSIGNED_BYTE,
                             self.tex_data)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            except:
                print("Cannot update texture")

    def __del__(self):
        glDeleteTextures(self.tex_id)

class Game(object):
    def __init__(self, config):
        self.config = config
        self.mode = "opengl"
        self.gl_surface = "plane"
        
        self.screen = None
        self.texture = None
        self.running = False

        self.game_field = field.GameField(config)
        
        self.current_block = None
        self.fall_speed = self.config.get_automatic_fall_start_speed()
        self.fall_field_counter = 0
        self.fall_speed_up_counter = 0
        
    def start(self):
        pygame.init()
		pygame.joystick.init()
		
		# Enumerate joysticks
        for i in range(0, pygame.joystick.get_count()):
            self.joystick_names.append(pygame.joystick.Joystick(i).get_name())
 
        print self.joystick_names
 
        # By default, load the first available joystick.
        if (len(self.joystick_names) > 0):
            self.my_joystick = pygame.joystick.Joystick(0)
            self.my_joystick.init()
 
        max_joy = max(self.my_joystick.get_numaxes(), 
                      self.my_joystick.get_numbuttons(), 
                      self.my_joystick.get_numhats())
        
        if self.mode == "fb":
            self.pyscope = pyscope.pyscope()
            self.screen = self.pyscope.screen
        elif self.mode == "pygame":
            self.screen = pygame.display.set_mode((self.config.get_field_size()[0] * (self.config.get_block_pixel_size()[0] +
                                                                                      self.config.get_block_pixel_padding()[0]) +
                                                   self.config.get_window_margin()[3] +
                                                   self.config.get_window_margin()[1],
                                                   self.config.get_field_size()[1] * (self.config.get_block_pixel_size()[1] +
                                                                                      self.config.get_block_pixel_padding()[1]) +
                                                   self.config.get_window_margin()[0] +
                                                   self.config.get_window_margin()[2]))
        elif self.mode == "opengl":
            self.tex_width, self.tex_height = (self.config.get_field_size()[0] * (self.config.get_block_pixel_size()[0] +
                                                                                  self.config.get_block_pixel_padding()[0]) +
                                               self.config.get_window_margin()[3] +
                                               self.config.get_window_margin()[1],
                                               self.config.get_field_size()[1] * (self.config.get_block_pixel_size()[1] +
                                                                                  self.config.get_block_pixel_padding()[1]) +
                                               self.config.get_window_margin()[0] +
                                               self.config.get_window_margin()[2])
            width, height = 1080, 1080

            if self.gl_surface == "cylinder":
                ratio = 2 * math.pi * 1.0 / 3.0
                self.tex_width = ratio * self.tex_height
            elif self.gl_surface == "plane":
                pass

            pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
            self.screen = pygame.Surface((self.tex_width, self.tex_height))

            self.gl_resize(width, height)
            self.gl_init()
        
        pygame.display.set_caption("Yayapytetris, here we go!")
        #pygame.display.update()
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(1, 100)
        
        self.game_loop()

    def gl_init(self):
        self.texture = Texture(self.screen)

        self.demanded_fps = 30.0

        self.gl_x = 0.0
        self.gl_y = 0.0

        self.gl_orbit_angle = 140.0

        self.gl_cam_elevation = 20.0
        self.gl_cam_distance = 16.0
        self.gl_cam_fov = 20.0
        self.gl_cam_aspect = 1.0

        self.gl_light_pos = [ 0.0, 1.0, 1.0 ]
        glShadeModel(GL_SMOOTH)
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_POSITION, self.gl_light_pos)

    def gl_resize(self, width, height):
        if height == 0:
            height = 1

        if width == 0:
            width = 1

        glViewport(0, 0, width, height)

        self.gl_cam_aspect = float(width) / float(height)

    def gl_draw(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.gl_cam_fov, self.gl_cam_aspect, 0.1, 1e3);

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        cam_x = 0.0 * self.gl_cam_distance
        cam_y = -math.cos(self.gl_cam_elevation * math.pi / 180) * self.gl_cam_distance
        cam_z = math.sin(self.gl_cam_elevation * math.pi / 180) * self.gl_cam_distance
        gluLookAt(cam_x, cam_y, cam_z, # cam
                      0,     0,     0, # target
                      0,     0,     1) # up
        glRotatef(self.gl_orbit_angle, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glColor3f(1.0, 1.0, 1.0)

        if self.gl_surface == "cyinder":
            glPushMatrix()
            glTranslatef(0.0, 0.0, -1.5)
            quad = gluNewQuadric()
            glBindTexture(GL_TEXTURE_2D, self.texture.tex_id)
            gluQuadricTexture(quad, GL_TRUE)
            gluCylinder(quad, 1.0, 1.0, 3.0, 50, 1)
            gluDeleteQuadric(quad)
            glPopMatrix()
        elif self.gl_surface == "plane":
            glBindTexture(GL_TEXTURE_2D, self.texture.tex_id)

            divider = 500.0

            glBegin(GL_QUADS)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(0.0, -self.tex_width / divider, self.tex_height / divider)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(0.0, -self.tex_width / divider, -self.tex_height / divider)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(0.0, self.tex_width / divider, -self.tex_height / divider)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(0.0, self.tex_width / divider, self.tex_height / divider)
            glEnd()

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
			elif event.type == JOYBUTTONDOWN:
				for i in range(self.my_joystick.get_numbuttons()):
					print(str(i) + ": " + str(self.my_joystick,get_button(i)))
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
            elif event.type == MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    rel_motion = pygame.mouse.get_rel()
                    self.gl_orbit_angle += rel_motion[0]
                    self.gl_cam_elevation += rel_motion[1]
                else:
                    # reset movement buffer
                    pygame.mouse.get_rel()
    
    def process_game_logic(self, delta_time):
        self.fall_field_counter += self.fall_speed * delta_time
        self.fall_speed_up_counter += delta_time
        
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
        self.screen.fill((0, 0, 0))

        self.game_field.draw(self.screen)
        self.current_block.draw(self.screen)

        if self.mode == "opengl":
            self.texture.update()
            self.gl_draw()

        pygame.display.flip()

    def process_sounds(self, delta_time):
        pass
    
    def generate_new_block(self):
        approximated_half_block_length = 1
        all_blocks = [blocks.I, blocks.WrongL, blocks.L, blocks.O, blocks.WrongN, blocks.T, blocks.N]
        color = (0, 0, 0)

        while color == (0, 0, 0):
            color = (random.randint(0, 1) * 255,
                     random.randint(0, 1) * 255,
                     random.randint(0, 1) * 255)

        self.current_block = all_blocks[random.randint(0, 6)](self.config,
                                                              (self.config.get_field_size()[0] / 2 - approximated_half_block_length, 0),
                                                              color)
