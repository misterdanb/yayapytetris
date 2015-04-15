class GameConfig(object):
    def __init__(self, display_type="pygame",
                 tilt_screen=False,
                 field_size=(10, 20),
                 block_pixel_size=(42, 42),
                 block_pixel_padding=(0, 0, 0, 0),
                 window_margin=(0, 0, 0, 0),
                 automatic_fall_start_speed=0.001,
                 automatic_fall_speed_up_step=0.0001,
                 automatic_fall_speed_up_time_step=10000):
        self.display_type = display_type
        
        self.tilt_screen = tilt_screen
        
        self.field_size = field_size
        
        self.block_pixel_size = block_pixel_size
        self.block_pixel_padding = block_pixel_padding
        self.window_margin = window_margin
        
        self.automatic_fall_start_speed = automatic_fall_start_speed
        self.automatic_fall_speed_up_step = automatic_fall_speed_up_step
        self.automatic_fall_speed_up_time_step = automatic_fall_speed_up_time_step
    
    def get_display_type(self):
        return self.display_type
    
    def get_tilt_screen(self):
        return self.tilt_screen
    
    def get_field_size(self):
        return self.field_size
    
    def get_block_pixel_size(self):
        return self.block_pixel_size
    
    def get_block_pixel_padding(self):
        return self.block_pixel_padding
    
    def get_window_margin(self):
        return self.window_margin
    
    def get_automatic_fall_start_speed(self):
        return self.automatic_fall_start_speed
    
    def get_automatic_fall_speed_up_step(self):
        return self.automatic_fall_speed_up_step
    
    def get_automatic_fall_speed_up_time_step(self):
        return self.automatic_fall_speed_up_time_step
