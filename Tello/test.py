import cv2, time, keyboard
import numpy as np
from djitellopy import Tello
import Geometry3D as geo
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from support import *
class Tester:
    def __init__(self) -> None:
        self.flight_path = Geometry3D.Segment(Geometry3D.Point([10, 10, 10]), Geometry3D.Point([200, 100, 100]))
        plt.ion()
    def graph(self):
        self.fig = plt.figure()
        # syntax for 3-D plotting
        self.ax = plt.axes(projection='3d')
        self.ax.set_title('Field')
        self.ax.set_xlim(0,472)
        self.ax.set_ylim(0,170)
        self.ax.set_zlim(0,200)
        self.ax.set_aspect('equal')
        self.ax.view_init(30, -130)
        move_figure(self.fig, 1500, 200)

        # syntax for plotting
        for hazard in HAZARD_LIST:
            if hazard[0] == 'c':
                Xc,Yc,Zc = data_for_cylinder_along_z(hazard[1][0], hazard[1][1], hazard[2], hazard[3])
                self.ax.plot_surface(Xc, Yc, Zc, alpha=0.5)

        Xc,Zc,Yc = data_for_cylinder_along_z(404, 90, 5, 70+50, 50)
        self.ax.plot_surface(Xc, Yc, Zc, alpha=0.5)
        Zc,Yc,Xc = data_for_cylinder_along_z(44, 40, 5, 70+54, 54)
        self.ax.plot_surface(Xc, Yc, Zc, alpha=0.5)
        plt.show()

    def graph_update(self):
        x, y, z = np.array([10, 200]), np.array([10, 100]), np.array([10, 100])
        self.ax.plot_surface(x, y, z)

    def close_graph(self):
        plt.close()

test = Tester()
test.graph()
time.sleep(7)
test.graph_update()