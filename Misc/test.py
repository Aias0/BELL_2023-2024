import keyboard, time, numpy, Geometry3D, matplotlib

flight_path = Geometry3D.Cylinder(Geometry3D.Point([10, 10, 10]), 10, Geometry3D.Vector(200, 50, 50))

r = Geometry3D.Renderer(backend='bell', args=[(472, 170, 200), 'avr'])
r.add((flight_path, 'red', 1), 0)

r.show()