from djitellopy import Tello
import math, sys, logging

class Bell_Tello(Tello):
    def __init__(self, field_length: int, field_width: int, field_height: int, start_pos: tuple, end_pos: tuple, hazards: list = []):
        super().__init__()
        self.field_length = field_length
        self.field_width = field_width
        self.field_height = field_height
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.hazards = hazards
        self.current_pos = (start_pos[0], start_pos[1] + self.__cm_inch(80))
        self.direction = 0
        # Pos: (x, y, z)
        # Hazards: (pos, radius, height)
        
        logging.basicConfig(level=logging.DEBUG)
    
    def move_pos(self, pos: tuple, order: tuple = ('z', 'y', 'x')):
        for axis in order:
            if axis == 'x':
                raw_move_x = pos[0] - self.current_pos[0]
                if 0 < self.current_pos[0] + raw_move_x < self.field_length:
                    can_move = True
                    for hazard in self.hazards:
                        if math.sqrt((self.current_pos[0] - hazard[0][0]) ** 2 + (self.current_pos[1] - hazard[0][1]) ** 2) < hazard[1] or hazard[2] > self.current_pos[2]:
                            can_move = False
                    move_x = self.__inch_cm(raw_move_x)
                    if can_move:
                        if move_x >= 20:
                            self.move_forward(int(move_x))
                        elif move_x <= -20:
                            self.move_back(int(abs(move_x)))
                        else:
                            logging.error(f'[error] ({self.current_pos} -> {pos} on x axis) move less than 20')
                    else:
                        logging.critical(f'[error] ({self.current_pos} -> {pos} on x axis) path ends in a hazard')
                else:
                    logging.warning(f'[error] ({self.current_pos} -> {pos} on x axis) postiton out of bounds')
            if axis == 'y':
                raw_move_y = pos[1] - self.current_pos[1]
                if 0 < self.current_pos[1] + raw_move_y < self.field_length:
                    can_move = True
                    for hazard in self.hazards:
                        if math.sqrt((self.current_pos[0] - hazard[0][0]) ** 2 + (self.current_pos[1] - hazard[0][1]) ** 2) < hazard[1] or hazard[2] > self.current_pos[2]:
                            can_move = False
                    move_y = self.__inch_cm(raw_move_y)
                    if can_move:
                        if move_y >= 20:
                            self.move_left(int(move_y))
                        elif move_y <= -20:
                            self.move_right(int(abs(move_y)))
                        else:
                            logging.error(f'[error] ({self.current_pos} -> {pos} on y axis) move less than 20')
                    else:
                        logging.critical(f'[error] ({self.current_pos} -> {pos} on y axis) path ends in a hazard')
                else:
                    logging.warning(f'[error] ({self.current_pos} -> {pos} on y axis) postiton out of bounds')
            if axis == 'z':
                raw_move_z = pos[2] - self.current_pos[2]
                if 0 < self.current_pos[2] + raw_move_z < self.field_length:
                    can_move = True
                    for hazard in self.hazards:
                        if math.sqrt((self.current_pos[0] - hazard[0][0]) ** 2 + (self.current_pos[1] - hazard[0][1]) ** 2) < hazard[1] or hazard[2] > self.current_pos[2]:
                            can_move = False
                    move_z = self.__inch_cm(raw_move_z)
                    if can_move:
                        if move_z >= 20:
                            self.move_up(int(move_z))
                        elif move_z <= -20:
                            self.move_down(int(abs(move_z)))
                        else:
                            logging.error(f'[error] ({self.current_pos} -> {pos} on z axis) move less than 20')
                    else:
                        logging.critical(f'[error] ({self.current_pos} -> {pos} on z axis) path ends in a hazard')
                else:
                    logging.warning(f'[error] ({self.current_pos} -> {pos} on z axis) postiton out of bounds')
                    
    def move_posS(self, postitions: list):
        for pos in postitions:
            if 1 < len(pos):
                self.move_pos(pos[0], pos[1])
            else:
                self.move_pos(pos)
            
    def land_pad(self):
        self.move_pos(self.end_pos)
        self.land()
    
    def get_pos(self) -> tuple:
        return self.current_pos
    def get_direction(self) -> str:
        dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        card_direction = round(self.direction / (360. / len(dirs)))
        return (self.direction, card_direction)
    
    def rotate_clockwise(self, x: int):
        self.direction += x
        if self.direction > 360:
            self.direction - 360
        return super().rotate_clockwise(x)
    def rotate_counter_clockwise(self, x: int):
        self.direction -= x
        if self.direction < 0:
            self.direction += 360
        return super().rotate_counter_clockwise(x)
    
    def __inch_cm(self, inch) -> float:
        return inch * 2.54
    def __cm_inch(self, cm) -> float:
        return cm / 2.54