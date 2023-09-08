import Geometry3D
field_length = 100
field_width = 100
field_height = 100

flight_path = Geometry3D.Segment(Geometry3D.Point([0, 0, 0]), Geometry3D.Point([10, 10, 10]))
hazard = Geometry3D.Cylinder(Geometry3D.Point(list((5, 20, 5))), 2, Geometry3D.Vector(0, 0, 15))

a = Geometry3D.Point(0, 0, 0)
b = Geometry3D.Point(field_length, 0, 0)
c = Geometry3D.Point(0, field_width, 0)
d = Geometry3D.Point(field_length, field_width, 0)
e = Geometry3D.Point(0, 0, field_height)
f = Geometry3D.Point(field_length, 0, field_height)
g = Geometry3D.Point(0, field_width, field_height)
h = Geometry3D.Point(field_length, field_width, field_height)
field_face0 = Geometry3D.ConvexPolygon((a, b, c, d))
field_face1 = Geometry3D.ConvexPolygon((a, b, f, e))
field_face2 = Geometry3D.ConvexPolygon((a, c, g, e))
field_face3 = Geometry3D.ConvexPolygon((c, d, h, g))
field_face4 = Geometry3D.ConvexPolygon((b, d, h, f))
field_face5 = Geometry3D.ConvexPolygon((e, f, h, g))
field = Geometry3D.ConvexPolyhedron((field_face0,field_face1,field_face2,field_face3,field_face4,field_face5))


test = Geometry3D.intersection(flight_path, hazard)
test2 = Geometry3D.intersection(Geometry3D.Point([50, 50, 50]), field)

print(f'Test1 = {bool(test)}\nTest2: {bool(test2)}')