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
    """  Pyhton wrapper for djitellopy. Allows for positional movement based on a defined field along with other miscellaneous functions."""
    def __init__(self, field_dimensions: tuple, start_pos: tuple, end_pos: tuple, hazards: list, tello_radius: float = 2.5):
        super().__init__()
        self.field_length = field_dimensions[0]
        self.field_width = field_dimensions[1]
        self.field_height = field_dimensions[2]
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.hazards = hazards
        self.tello_rad = tello_radius
        self.current_pos = [start_pos[0], start_pos[1], start_pos[2] + cm_inch(80)] # Make sure to account for takeoff height
        self.direction = 0
        self.camera_forward = True
        self.speed = 0
        # Pos: (x, y, z)
        # Hazards: (pos, radius, height)
        self.axis_vals = {'x': 0, 'y': 1, 'z': 2}
        # Graphing Setup
        self.graph_thread = Thread(target=self.graph)
        self.graph_thread.start()
 
    def move_pos(self, pos: tuple, speed: int = 50):
        """ Move Tello to position in 3D space. Moves in a line. Rerouts flight path around hazards, will not move if flight path ends out of bounds. Speed is in cm/s
        Arguments:
            speed: 10-100 (Defaults to 50)"""
        self.speed = speed
        relative_pos = [0, 0, 0]
        for i in range(3):
            relative_pos[i] = inch_cm(pos[i] - self.current_pos[i])
        print(relative_pos)
        path_clear = True
        flight_path = Geometry3D.Cylinder(Geometry3D.Point(list(self.current_pos)), self.tello_rad, Geometry3D.Vector(np.subtract(pos, self.current_pos)))
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
                    print('More than 500')
                    relative_pos[idx] =- 500 * axis/abs(axis) * -1
                    extra_pos[idx] = relative_pos[idx] - 500 * axis/abs(axis) * -1
            # Move to position
            print(f'Moving: {pos} | {relative_pos}')
            self.go_xyz_speed(int(relative_pos[0]), int(relative_pos[1]), int(relative_pos[2]), int(speed))
            self.current_pos = pos
            # Move leftover
            if max(extra_pos) != 0:
                self.go_xyz_speed(extra_pos[0], extra_pos[1], extra_pos[2], speed)
        else:
            # Pathfinding
            logging.info(f'({self.current_pos} -> {pos}) Path rerouted.')
            print(f'Moving: {(hazard[1][0], hazard[1][1], hazard[3] + 10)}')
            self.move_pos((hazard[1][0], hazard[1][1], hazard[3] + 10))
            self.current_pos = (hazard[1][0], hazard[1][1], hazard[3] + 10)
            print(f'Moving: {pos}')
            self.move_pos(pos)
            self.current_pos = pos
        
    def move_pos_mult(self, positions: list, speed: int = 50):
        """ Move Tello to multiple positions in 3D space. Moves in a line. Uses move_pos. Speed is in cm/s
        Arguments:
            speed: 10-100 (Defaults to 50)"""
        self.speed = speed
        for pos in positions:
            self.move_pos(pos, speed)


    def land_building_pad(self):
        """ Moves Tello to end postition then lands. """
        self.move_pos((self.end_pos[0], self.end_pos[1], self.end_pos[2]+10))
        time.sleep(1)
        self.land()
        
    def land_ground_pad(self):
        """ Moves Tello to start postition then lands. """
        self.move_pos((self.start_pos[0], self.start_pos[1], self.start_pos[2]+10))
        time.sleep(1)
        self.land()
        
    def payload_release(self):
        """ [Under Construction] Releases payload. """
        print('payload released')
    
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
        card_direction = dirs[round(self.direction / (360. / len(dirs)))]
        return (card_direction, self.direction)
    
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
    
    def set_video_direction(self, x: int):
        self.camera_forward = not bool(x)
        super().set_video_direction(x)
    def toggle_video_direction(self):
        self.set_video_direction(int(not self.camera_forward))
        
    # Graphing            
    def graph(self):
        self.fig = plt.figure()

        # Define plot size
        ax = plt.axes(projection='3d')
        ax.set_title('Field')
        ax.set_xlim(0, self.field_length)
        ax.set_ylim(0, self.field_width)
        ax.set_zlim(0, self.field_height)
        ax.set_aspect('equal')
        # Move window and set view
        ax.view_init(30, -130)
        move_figure(self.fig, 1500, 200)
    
        # Plot buildings
        for hazard in HAZARD_LIST:
            if hazard[0] == 'c':
                Xc,Yc,Zc = data_for_cylinder_along_z(hazard[1][0], hazard[1][1], hazard[2], hazard[3])
                ax.plot_surface(Xc, Yc, Zc, alpha=0.5)
        #Plot crossways
        Xc,Zc,Yc = data_for_cylinder_along_z(404, 90, 5, 70+50, 50)
        ax.plot_surface(Xc, Yc, Zc, alpha=0.5)
        Zc,Yc,Xc = data_for_cylinder_along_z(44, 40, 5, 70+54, 54)
        ax.plot_surface(Xc, Yc, Zc, alpha=0.5)
        # Show plot
        plt.show()
        
    def close_graph(self):
        plt.close()
    
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
           