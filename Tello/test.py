import Geometry3D
flight_path = Geometry3D.Segment(Geometry3D.Point([0, 0, 0]), Geometry3D.Point([10, 10, 10]))

print(flight_path.__getitem__(0))