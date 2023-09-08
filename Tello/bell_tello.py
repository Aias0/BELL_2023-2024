from djitellopy import Tello
import numpy as np
import matplotlib.pyplot as plt
import math, sys, os, logging, datetime, ladybug_geometry, Geometry3D
from data import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(filename=f'Logs\Log{LOG_NUM}_{datetime.date.isoformat(datetime.date.today())}_{datetime.datetime.now().strftime("%H-%M-%S")}.log', filemode='w', format='%(asctime)s-%(levelname)s-%(message)s', level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())
LOG_NUM += 1
with open('data.py', 'r+') as f:
    f.write(f'LOG_NUM = {LOG_NUM}')

class Bell_Tello(Tello):
    def __init__(self, field_length: int, field_width: int, field_height: int, start_pos: tuple, end_pos: tuple, hazards: list = []):
        super().__init__()
        logging.debug('init')
        self.field_length = field_length
        self.field_width = field_width
        self.field_height = field_height
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.hazards = hazards
        self.current_pos = (start_pos[0], start_pos[1] + int(self.__cm_inch(80)), start_pos[2]) # Make sure to account for takeoff height
        self.direction = 0
        # Pos: (x, y, z)
        # Hazards: (pos, radius, height)
        self.axis_vals = {'x': 0, 'y': 1, 'z': 2}
        self.default_speed = 50
 
    def move_pos_line(self, pos: tuple, speed: int = None):
        """ Move Tello to position in 3D space. Moves in a line. Will not move if flight path intersects a hazard or ends out of bounds. Speed is in cm/s
        Arguments:
            speed: 10-100 (Defaults to 50)"""
        self.speed = speed or self.default_speed
        relative_pos = self.__inch_cm(tuple(map(lambda i, j: i - j, pos, self.current_pos)))
        self.can_fly = True
        flight_path = Geometry3D.Segment(Geometry3D.Point(list(self.current_pos)), Geometry3D.Point(list(pos)))
        field = self.geo3D_rect(
            (0, 0, 0),
            (self.field_length, 0, 0),
            (0, self.field_width, 0),
            (self.field_length, self.field_width, 0),
            (0, 0, self.field_height),
            (self.field_length, 0, self.field_height),
            (0, self.field_width, self.field_height),
            (self.field_length, self.field_width, self.field_height)
        )
        if not Geometry3D.intersection(Geometry3D.Point(list(pos)), field):
            can_fly = False
            logging.warning(f'({self.current_pos} -> {pos}) Results in tello moving out of bounds, comand canceled.')
        for hazard in self.hazards:
            if Geometry3D.intersection(flight_path, Geometry3D.Cylinder(Geometry3D.Point(list(hazard[0])), hazard[1], Geometry3D.Vector(0, 0, hazard[2]))):
                can_fly = False
                logging.warning(f'({self.current_pos} -> {pos}) Results in tello hitting hazard, path rerouted.')
        if can_fly:
            self.go_xyz_speed(relative_pos[0], relative_pos[1], relative_pos[2], speed)
            self.current_pos = pos
        
    
    def move_pos_line_mult(self, positions: list, speed: int = None):
        """ Move Tello to multiple positions in 3D space. Moves in a line. Uses move_pos_line. Speed is in cm/s
        Arguments:
            speed: 10-100 (Defaults to 50)"""
        self.speed = speed or self.default_speed
        for pos in positions:
            self.move_pos_line(pos, speed)


    def land_pad(self):
        """ Moves Tello to end postition then lands. """
        self.move_pos_line(self.end_pos)
        self.land()
    
    def get_pos(self) -> tuple:
        """ Gets Tello's current position on field.
        Returns: 
            tuple: (x, y, z)"""
        return self.current_pos
    def get_direction(self) -> str:
        """ Gets Tello's current direction.
        Returns:
            tuple: (degree, cardinal). """
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
    
    def __inch_cm(self, inch):
        """ Returns float for int or float. Returns tuple for tuple. """
        if type(inch) is int or type(inch) is float:
            return inch * 2.54
        elif type(inch) is tuple:
            return (self.__inch_cm(inch[0]), self.__inch_cm(inch[1]), self.__inch_cm(inch[2]))
        return None
    def __cm_inch(self, cm):
        """ Returns float for int or float. Returns tuple for tuple. """
        if type(cm) is int or type(cm) is float:
            return cm / 2.54
        elif type(cm) is tuple:
            return (self.__inch_cm(cm[0]), self.__inch_cm(cm[1]), self.__inch_cm(cm[2]))
        return None
    
    def geo3D_rect(a: tuple, b: tuple, c: tuple, d: tuple, e: tuple, f: tuple, g: tuple, h: tuple):
        a = Geometry3D.Point(list(a))
        b = Geometry3D.Point(list(b))
        c = Geometry3D.Point(list(c))
        d = Geometry3D.Point(list(d))
        e = Geometry3D.Point(list(e))
        f = Geometry3D.Point(list(f))
        g = Geometry3D.Point(list(g))
        h = Geometry3D.Point(list(h))
        field_face0 = Geometry3D.ConvexPolygon((a, b, c, d))
        field_face1 = Geometry3D.ConvexPolygon((a, b, f, e))
        field_face2 = Geometry3D.ConvexPolygon((a, c, g, e))
        field_face3 = Geometry3D.ConvexPolygon((c, d, h, g))
        field_face4 = Geometry3D.ConvexPolygon((b, d, h, f))
        field_face5 = Geometry3D.ConvexPolygon((e, f, h, g))
        return Geometry3D.ConvexPolyhedron((field_face0,field_face1,field_face2,field_face3,field_face4,field_face5))
    
    # Methods Deprecated    
    def move_pos_axis(self, pos: tuple, order: tuple = ('z', 'y', 'x')):
        """ [DEPRECATED] Move Tello to position in 3D space. Moves one axis at a time. Will not move if position ends at a hazard or out of bounds. """
        for axis in order:
            raw_move = pos[self.axis_vals[axis]] - self.current_pos[self.axis_vals[axis]]
            if 0 < self.current_pos[self.axis_vals[axis]] + raw_move < self.field_length:
                can_move = True
                for hazard in self.hazards:
                    if math.sqrt((self.current_pos[0] - hazard[0][0]) ** 2 + (self.current_pos[1] - hazard[0][1]) ** 2) < hazard[1] or hazard[2] > self.current_pos[2]:
                        can_move = False
                move = int(self.__inch_cm(raw_move))
                if can_move:
                    if move >= 20:
                        if axis == 'x':
                            self.move_forward(move)
                        elif axis == 'y':
                            self.move_left(move)
                        elif axis == 'z':
                            self.move_up(move)
                    elif move <= -20:
                        if axis == 'x':
                            self.move_back(abs(move))
                        elif axis == 'y':
                            self.move_right(abs(move))
                        elif axis == 'z':
                            self.move_down(abs(move))
                    else:
                        logging.error(f'({self.current_pos} -> {pos} on {axis} axis) move less than 20')
                    self.current_pos[self.axis_vals[axis]] += move
                else:
                    logging.critical(f'({self.current_pos} -> {pos} on {axis} axis) path ends in a hazard')
            else:
                logging.warning(f'({self.current_pos} -> {pos} on {axis} axis) postiton out of bounds')
    def move_pos_axis_mult(self, postitions: list):
        """ [DEPRECATED] Move Tello to multiple positions in 3D space. Moves one axis at a time. Uses move_pos_axis. """
        for pos in postitions:
            if 1 < len(pos):
                self.move_pos_axis(pos[0], pos[1])
            else:
                self.move_pos_axis(pos)
           