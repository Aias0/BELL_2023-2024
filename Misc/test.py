import keyboard, time, numpy, Geometry3D, matplotlib, sys
import numpy as np
sys.path.insert(1, 'Common_Data/')
HAZARD_LIST = None
from data import *
flight_path = Geometry3D.Cylinder(Geometry3D.Point([10, 10, 10]), 20, Geometry3D.Vector(200, 50, 50), 20)
r = Geometry3D.Renderer(backend='bell', args=[(472, 170, 200), 'avr'])
#r.add((flight_path, 'red', 1), 0)

#for hazard in HAZARD_LIST:
#    r.add((Geometry3D.Cylinder(Geometry3D.Point(list(hazard[0])), hazard[1], Geometry3D.Vector(list(hazard[2]))), 'green', 1))
r.add((Geometry3D.Plane(Geometry3D.Point(292, 0, 0), Geometry3D.Point(472, 0, 48), Geometry3D.Point(472, 170, 48)), 'blue', 1))
r.show()
""" 
import numpy as np
import matplotlib.pyplot as plt
points = [[0, 0, 0], [200, 0, 200], [200, 200, 200]]
p0, p1, p2 = points
x0, y0, z0 = p0
x1, y1, z1 = p1
x2, y2, z2 = p2
ux, uy, uz = u = [x1-x0, y1-y0, z1-z0]
vx, vy, vz = v = [x2-x0, y2-y0, z2-z0]
u_cross_v = [uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx]
point  = np.array(p0)
normal = np.array(u_cross_v)
d = -point.dot(normal)
xx, yy = np.meshgrid(range(10), range(10))
z = (-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2]

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.plot_surface(xx, yy, z)
plt.show() """