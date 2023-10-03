from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from data import *
import matplotlib.pyplot as plt
import Geometry3D
 
def inch_cm(inch):
    """ Inch -> Cm. Returns float for int or float. Returns tuple for tuple. """
    if type(inch) is int or type(inch) is float:
        return inch * 2.54
    elif type(inch) is list:
        return [inch_cm(inch[0]), inch_cm(inch[1]), inch_cm(inch[2])]
def cm_inch(cm):
    """ Cm -> Inch. Returns float for int or float. Returns tuple for tuple. """
    if type(cm) is int or type(cm) is float:
        return cm / 2.54
    elif type(cm) is list:
        return [inch_cm(cm[0]), inch_cm(cm[1]), inch_cm(cm[2])]
 
def data_for_cylinder_along_z(center_x,center_y,radius,height_z, start_z = 0):
    z = np.linspace(start_z, height_z, 50)
    theta = np.linspace(0, 2*np.pi, 50)
    theta_grid, z_grid=np.meshgrid(theta, z)
    x_grid = radius*np.cos(theta_grid) + center_x
    y_grid = radius*np.sin(theta_grid) + center_y
    return x_grid,y_grid,z_grid

def cuboid_data(center, size):
    # suppose axis direction: x: to left; y: to inside; z: to upper
    # get the (left, outside, bottom) point
    o = [a - b / 2 for a, b in zip(center, size)]
    # get the length, width, and height
    l, w, h = size
    x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]],  # x coordinate of points in bottom surface
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],  # x coordinate of points in upper surface
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],  # x coordinate of points in outside surface
         [o[0], o[0] + l, o[0] + l, o[0], o[0]]]  # x coordinate of points in inside surface
    y = [[o[1], o[1], o[1] + w, o[1] + w, o[1]],  # y coordinate of points in bottom surface
         [o[1], o[1], o[1] + w, o[1] + w, o[1]],  # y coordinate of points in upper surface
         [o[1], o[1], o[1], o[1], o[1]],          # y coordinate of points in outside surface
         [o[1] + w, o[1] + w, o[1] + w, o[1] + w, o[1] + w]]    # y coordinate of points in inside surface
    z = [[o[2], o[2], o[2], o[2], o[2]],                        # z coordinate of points in bottom surface
         [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],    # z coordinate of points in upper surface
         [o[2], o[2], o[2] + h, o[2] + h, o[2]],                # z coordinate of points in outside surface
         [o[2], o[2], o[2] + h, o[2] + h, o[2]]]                # z coordinate of points in inside surface
    return x, y, z

def move_figure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = plt.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)


def geo3D_rect(length: int, width: int, height: int):
    """ function that creates a 3d rectangle based on the length, width and heigh parameters """
    a = Geometry3D.Point(list((0, 0, 0)))
    b = Geometry3D.Point(list((length, 0, 0)))
    c = Geometry3D.Point(list((0, width, 0)))
    d = Geometry3D.Point(list((length, width, 0)))
    e = Geometry3D.Point(list((0, 0, height)))
    f = Geometry3D.Point(list((length, 0, height)))
    g = Geometry3D.Point(list((0, width, height)))
    h = Geometry3D.Point(list((length, width, height)))
    field_face0 = Geometry3D.ConvexPolygon((a, b, c, d))
    field_face1 = Geometry3D.ConvexPolygon((a, b, f, e))
    field_face2 = Geometry3D.ConvexPolygon((a, c, g, e))
    field_face3 = Geometry3D.ConvexPolygon((c, d, h, g))
    field_face4 = Geometry3D.ConvexPolygon((b, d, h, f))
    field_face5 = Geometry3D.ConvexPolygon((e, f, h, g))
    return Geometry3D.ConvexPolyhedron((field_face0,field_face1,field_face2,field_face3,field_face4,field_face5))