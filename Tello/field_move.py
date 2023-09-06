from djitellopy import Tello
import math

class Field(Tello):
    def __init__(self, length: int, width: int, height: int, start_pos: tuple, end_pos: tuple, hazards: list = []):
        super().__init__()
        self.length = length
        self.width = width
        self.height = height
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.hazards = hazards
        self.current_pos = start_pos
        # Pos: (x, y, z)
        # Hazards: (pos, radius, height)
    
    def move_pos(self, pos: tuple, order: tuple = ('z', 'y', 'x')):
        for axis in order:
            if axis == 'x':
                raw_move_x = pos[0] - self.current_pos[0]
                if (0 < self.current_pos[0] + raw_move_x < self.length) and (self.current_pos[2] > [hazard[2] for hazard in self.hazards]):
                    can_move = True
                    for hazard in self.hazards:
                        if math.sqrt((self.current_pos[0] - hazard[0][0]) ** 2 + (self.current_pos[1] - hazard[0][1]) ** 2) < hazard[1]:
                            can_move = False
                    move_x = self.__inch_cm(raw_move_x)
                    if can_move:
                        if move_x >= 20:
                            self.move_forward(int(move_x))
                        elif move_x <= -20:
                            self.move_back(int(abs(move_x)))
                        else:
                            print('[error] move less than 20')
                else:
                    print('[error] postiton out of bounds')
            if axis == 'y':
                raw_move_y = pos[1] - self.current_pos[1]
                if (0 < self.current_pos[1] + raw_move_y < self.length) and (self.current_pos[2] > [hazard[2] for hazard in self.hazards]):
                    can_move = True
                    for hazard in self.hazards:
                        if math.sqrt((self.current_pos[0] - hazard[0][0]) ** 2 + (self.current_pos[1] - hazard[0][1]) ** 2) < hazard[1]:
                            can_move = False
                    move_y = self.__inch_cm(raw_move_y)
                    if can_move:
                        if move_y >= 20:
                            self.move_left(int(move_y))
                        elif move_y <= -20:
                            self.move_right(int(abs(move_y)))
                        else:
                            print('[error] move less than 20')
                else:
                    print('[error] postiton out of bounds')
            if axis == 'z':
                raw_move_z = pos[2] - self.current_pos[2]
                if (0 < self.current_pos[2] + raw_move_z < self.length) and (self.current_pos[2] > [hazard[2] for hazard in self.hazards]):
                    can_move = True
                    for hazard in self.hazards:
                        if math.sqrt((self.current_pos[0] - hazard[0][0]) ** 2 + (self.current_pos[1] - hazard[0][1]) ** 2) < hazard[1]:
                            can_move = False
                    move_z = self.__inch_cm(raw_move_z)
                    if can_move:
                        if move_z >= 20:
                            self.move_up(int(move_z))
                        elif move_z <= -20:
                            self.move_down(int(abs(move_z)))
                        else:
                            print('[error] move less than 20')
                else:
                    print('[error] postiton out of bounds')
            
    def land_pad(self):
        self.move_pos(self.end_pos)
        self.land()

    def get_pos(self):
        return self.current_pos
    
    def __inch_cm(self, inch):
        return inch * 2.54