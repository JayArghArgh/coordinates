import math


# Do the math
class CalculateCoordinates:
    def __init__(self):
        self.from_coordinates = [0, 0, 0]
        self.to_coordinates = [0, 0, 0]
        self.bearing = 0.0
        self.distance_2d = 0.0
        self.distance_3d = 0.0
        self.delta_e = 0.0
        self.delta_n = 0.0
        self.delta_el = 0.0
        self.feature_code = ""

    def set_feature_code(self, feature_code):
        self.feature_code = feature_code

    def get_feature_code(self):
        return self.feature_code

    def set_deltas_from_coordinates(self):
        # difference between both sets of coordinates.
        self.delta_e = self.from_coordinates[0] - self.to_coordinates[0]
        self.delta_n = self.from_coordinates[1] - self.to_coordinates[1]
        self.delta_el = self.from_coordinates[2] - self.to_coordinates[2]

    def set_deltas_from_bearing_distance(self):
        # Creates deltas from bearing and distance
        self.delta_e = self.distance_2d * (math.sin(math.radians(self.bearing)))
        self.delta_n = self.distance_2d * (math.cos(math.radians(self.bearing)))
        # print(f"shifting dist: {self.distance_2d}")
        # print(f"shifting bearing: {self.bearing}")
        # print(f"delta e: {self.delta_e}, delta n: {self.delta_n}")
        # TODO requires vertical bearing and distance for delta_el.

    def set_deltas(self, delta_e, delta_n, delta_el):
        # Manually set the deltas
        self.delta_e = delta_e
        self.delta_n = delta_n
        self.delta_el = delta_el

    def set_coordinates_from_deltas(self):
        # Create new coords from deltas.
        self.to_coordinates[0] = self.from_coordinates[0] - self.delta_e
        self.to_coordinates[1] = self.from_coordinates[1] - self.delta_n
        self.to_coordinates[2] = self.from_coordinates[2] - self.delta_el

    def set_from_coordinates(self, coord_array):
        self.from_coordinates = coord_array

    def get_from_coordinates(self):
        return self.from_coordinates

    def get_to_coordinates(self):
        return self.to_coordinates

    def set_to_coordinates(self, coord_array):
        self.to_coordinates = coord_array

    def set_bearing_from_coordinates(self):
        # A great big switch statement to determine the correct direction.
        if self.delta_e == 0 and self.delta_n > 0:
            self.bearing = 0.0
        elif self.delta_e == 0 and self.delta_n < 0:
            self.bearing = 180.0
        elif self.delta_e > 0 and self.delta_n == 0:
            self.bearing = 90.0
        elif self.delta_e < 0 and self.delta_n == 0:
            self.bearing = 270.0

        # Check for 45 degree variations.
        elif abs(self.delta_e) == abs(self.delta_n):
            if self.delta_e > 0 and self.delta_n > 0:
                self.bearing = 45.0
            elif self.delta_e > 0 > self.delta_n:
                self.bearing = 135.0
            elif self.delta_e < 0 and self.delta_n < 0:
                self.bearing = 225.0
            elif self.delta_n > 0 > self.delta_e:
                self.bearing = 315.0

        # Compute it out.
        elif self.delta_e > 0:
            self.bearing = math.degrees(math.atan(self.delta_e / self.delta_n))
        elif self.delta_e < 0 and self.delta_n < 0:
            self.bearing = math.degrees(math.atan(self.delta_e / self.delta_n)) + 180
        elif self.delta_n > 0 > self.delta_e:
            self.bearing = math.degrees(math.atan(self.delta_e / self.delta_n)) + 360

        # The final piece.
        if self.bearing < 0:
            self.bearing += 180

    def set_bearing(self, bearing):
        self.bearing = bearing

    def get_bearing(self):
        return self.bearing

    def set_distance_2d_from_deltas(self):
        # Determine the distance. (2D)
        self.distance_2d = math.sqrt((self.delta_e ** 2 + self.delta_n ** 2))

    def set_distance_2d(self, distance_2d):
        self.distance_2d = distance_2d

    def get_distance_2d(self):
        return self.distance_2d

    def set_distance_3d_from_deltas(self):
        # Determine the distance. (3D)
        self.distance_3d = math.sqrt(self.delta_e ** 2 + self.delta_n ** 2 + self.delta_el ** 2)

    def set_distance_3d(self, distance_3d):
        self.distance_3d = distance_3d

    def get_distance_3d(self):
        return self.distance_3d

    def set_bearing_distance_from_coordinates(self):
        # Return bearing and distance derived from two sets of coordinates.
        self.set_deltas_from_coordinates()
        self.set_bearing_from_coordinates()
        self.set_distance_2d_from_deltas()
        self.set_distance_3d_from_deltas()

    def set_coordinates_from_bearing_and_distance(self):
        self.set_deltas_from_bearing_distance()
        # print(f"from {self.from_coordinates}")
        self.set_coordinates_from_deltas()
        # print(f"to {self.to_coordinates}")
