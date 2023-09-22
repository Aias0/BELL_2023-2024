import cv2, time, keyboard
import numpy as np
from djitellopy import Tello
import Geometry3D as geo
import matplotlib.pyplot as plt
from support import *
class Tester:
    def __init__(self) -> None:
        pass
    def graph(self):
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

test = Tester()
test.graph()
