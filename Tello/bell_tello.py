from djitellopy import Tello
from mpl_toolkits import mplot3d
from threading import Thread
from support import *
import numpy as np
import matplotlib.pyplot as plt
import math, sys, os, logging, datetime, Geometry3D, time
from data import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(filename=f'Logs\Log{LOG_NUM}_{datetime.date.isoformat(datetime.date.today())}_{datetime.datetime.now().strftime("%H-%M-%S")}.log', filemode='w', format='%(asctime)s-%(levelname)s-%(message)s', level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler())
LOG_NUM += 1
with open('data.py', 'r+') as f:
    f.write(f'LOG_NUM = {LOG_NUM}')

class Bell_Tello(Tello):
    """  Wrapper for djitellopy. Allows for positional movement based on a defined field along with other miscellaneous functions."""
    def __init__(self, field_length: int, field_width: int, field_height: int, start_pos: tuple, end_pos: tuple, hazards: list):
        super().__init__()
        self.field_length = field_length
        self.field_width = field_width
        self.field_height = field_height
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.hazards = hazards
        self.current_pos = (start_pos[0], start_pos[1], start_pos[2] + cm_inch(80)) # Make sure to account for takeoff height
        print(self.current_pos)
        self.direction = 0
        # Pos: (x, y, z)
        # Hazards: (pos, radius, height)
        self.axis_vals = {'x': 0, 'y': 1, 'z': 2}
        self.default_speed = 50
        
        # Graphing Setup
        self.graph_thread = Thread(target=self.graph)
        self.graph_thread.start()
 
    def move_pos_line(self, pos: tuple, speed: int = 50):
        """ Move Tello to position in 3D space. Moves in a line. Rerouts flight path around hazards, will not move if flight path ends out of bounds. Speed is in cm/s
        Arguments:
            speed: 10-100 (Defaults to 50)"""
        self.speed = speed
        relative_pos = [0, 0, 0]
        for i in range(3):
            relative_pos[i] = inch_cm(pos[i] - self.current_pos[i])
        print(relative_pos)
        path_clear = True
        flight_path = Geometry3D.Segment(Geometry3D.Point(list(self.current_pos)), Geometry3D.Point(list(pos)))
        field = geo3D_rect(self.field_length, self.field_width, self.field_height)
        # Check flightpath for obstacles
        if not Geometry3D.intersection(Geometry3D.Point(list(pos)), field):
            path_clear = False
            logging.warning(f'({self.current_pos} -> {pos}) Results in tello moving out of bounds, comand canceled.')
        for hazard in self.hazards:
            if hazard[0] == 'c' and Geometry3D.intersection(flight_path, Geometry3D.Cylinder(Geometry3D.Point(list(hazard[1])), hazard[2], Geometry3D.Vector(0, 0, hazard[3]))):
                path_clear = False
                logging.warning(f'({self.current_pos} -> {pos}) Results in tello hitting hazard, path rerouting.')
            
        if path_clear:
            # Check to see if move command is above out of range(-500-500)
            extra_pos = [0, 0, 0]
            for idx, axis in enumerate(relative_pos):
                if abs(axis) > 500:
                    relative_pos[idx] =- 500 * axis/abs(axis)
                    extra_pos[idx] = relative_pos[idx] - 500 * axis/abs(axis)
            # Move to position
            print(f'Moving: {pos}')
            self.go_xyz_speed(int(relative_pos[0]), int(relative_pos[1]), int(relative_pos[2]), int(speed))
            self.current_pos = pos
            if max(extra_pos) != 0:
                self.go_xyz_speed(extra_pos[0], extra_pos[1], extra_pos[2], speed)
        else:
            # Pathfinding
            logging.info(f'({self.current_pos} -> {pos}) Path rerouted.')
            print(f'Moving: {(hazard[1][0], hazard[1][1], hazard[3] + 10)}')
            self.move_pos_line((hazard[1][0], hazard[1][1], hazard[3] + 10))
            self.current_pos = (hazard[1][0], hazard[1][1], hazard[3] + 10)
            print(f'Moving: {pos}')
            self.move_pos_line(pos)
            self.current_pos = pos
        
    def move_pos_line_mult(self, positions: list, speed: int = 50):
        """ Move Tello to multiple positions in 3D space. Moves in a line. Uses move_pos_line. Speed is in cm/s
        Arguments:
            speed: 10-100 (Defaults to 50)"""
        self.speed = speed
        for pos in positions:
            self.move_pos_line(pos, speed)


    def land_pad(self):
        """ Moves Tello to end postition then lands. """
        self.move_pos_line(self.end_pos)
        time.sleep(1)
        self.land()
        self.close_graph()
    
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
    
    # Graphing            
    def graph(self):
        # defining surface and axes
        x = np.outer(np.linspace(-2, 2, 10), np.ones(10))
        y = x.copy().T
        z = np.cos(x ** 2 + y ** 3)

        self.fig = plt.figure()

        # syntax for 3-D plotting
        ax = plt.axes(projection='3d')
        ax.set_title('Field')
        ax.set_xlim(0,472)
        ax.set_ylim(0,170)

        ax.set_zlim(0,200)
        ax.set_aspect('equal')
        ax.view_init(30, -130)
        move_figure(self.fig, 1500, 200)
    
        # syntax for plotting
        for hazard in HAZARD_LIST:
            if hazard[0] == 'c':
                Xc,Yc,Zc = data_for_cylinder_along_z(hazard[1][0], hazard[1][1], hazard[2], hazard[3])
                ax.plot_surface(Xc, Yc, Zc, alpha=0.5)
        
        Xc,Zc,Yc = data_for_cylinder_along_z(404, 90, 5, 70+50, 50)
        ax.plot_surface(Xc, Yc, Zc, alpha=0.5)
        Zc,Yc,Xc = data_for_cylinder_along_z(44, 40, 5, 70+54, 54)
        ax.plot_surface(Xc, Yc, Zc, alpha=0.5)
        plt.show()
        
    def close_graph(self):
        plt.close()
        self.graph_thread.join()
    
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
                move = int(inch_cm(raw_move))
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
           