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
    """
       Create a data array for cuboid plotting.


       ============= ================================================
       Argument      Description
       ============= ================================================
       center        center of the cuboid, triple
       size          size of the cuboid, triple, (x_length,y_width,z_height)
       :type size: tuple, numpy.array, list
       :param size: size of the cuboid, triple, (x_length,y_width,z_height)
       :type center: tuple, numpy.array, list
       :param center: center of the cuboid, triple, (x,y,z)
      """
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
""" 
# defining surface and axes
x = np.outer(np.linspace(-2, 2, 10), np.ones(10))
y = x.copy().T
z = np.cos(x ** 2 + y ** 3)
 
fig = plt.figure()
 
# syntax for 3-D plotting
ax = plt.axes(projection='3d')
ax.set_xlim(0,472)
ax.set_ylim(0,170)

ax.set_zlim(0,200)
ax.set_aspect('equal')
ax.view_init(30, -130)
move_figure(fig, 1500, 200)
ax.set_title('Field')

# syntax for plotting
for hazard in HAZARD_LIST:  
    Xc,Yc,Zc = data_for_cylinder_along_z(hazard[1][0], hazard[1][1], hazard[2], hazard[3])
    ax.plot_surface(Xc, Yc, Zc, alpha=0.5)

Xc,Zc,Yc = data_for_cylinder_along_z(404, 90, 5, 70+50, 50)
ax.plot_surface(Xc, Yc, Zc, alpha=0.5)
Zc,Yc,Xc = data_for_cylinder_along_z(44, 40, 5, 70+54, 54)
ax.plot_surface(Xc, Yc, Zc, alpha=0.5)

x = np.linspace(292, 472, 100)
y = np.linspace(0, 170, 100)
x, y = np.meshgrid(x, y)
eq = 0.12 * x + 0.01 * y + 1.09
ax.plot_surface(x, y, eq)

plt.show() """