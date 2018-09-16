import math
from functools import reduce


class Utils:
    @staticmethod
    def compute_min_distance(point_a, point_b, point_c):
        pa_x, pa_y, pa_z = point_a
        pb_x, pb_y, pb_z = point_b
        pc_x, pc_y, pc_z = point_c
        vector_ba = (pa_x - pb_x, pa_y - pb_y, pa_z - pb_z)
        vector_bc = (pc_x - pb_x, pc_y - pb_y, pc_z - pb_z)
        ba_cross_bc = [vector_ba[1] * vector_bc[2] - vector_ba[2] * vector_bc[1],
                       vector_ba[2] * vector_bc[0] - vector_ba[0] * vector_bc[2],
                       vector_ba[0] * vector_bc[1] - vector_ba[1] * vector_bc[0]]
        modulus_bc = math.sqrt(reduce(lambda x, y: x + y, map(lambda x: x ** 2, vector_bc)))
        modulus_ba_cross_bc = math.sqrt(reduce(lambda x, y: x + y, map(lambda x: x ** 2, ba_cross_bc)))
        return modulus_ba_cross_bc / modulus_bc


if __name__ == '__main__':
    print(Utils.compute_min_distance((1, 2, 3), (2, 1, 2), (1, 1, 1)))
    print(Utils.compute_min_distance((0, 0, 0), (0, 1, 0), (1, 0, 0)))