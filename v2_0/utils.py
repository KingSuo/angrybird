import math
from functools import reduce

import numpy as np

from const import Z_RANGE, RADAR_POINTS, FAKE_POINTS, TIME_INTERVAL
from code import Code


class Utils:
    @staticmethod
    def get_distances_by_multi_points(point1, point2, point3_list):
        """

        :param point1:
        :param point2:
        :param point3_list:
        :return:
        """
        return [Utils.get_distance_by_3points(point1, point2, point3) for point3 in point3_list]

    @staticmethod
    def get_distance_by_3points(point1, point2, point3):
        """
        Get distance which is point1 to line that through point2 & point3
        :param point1:
        :param point2:
        :param point3:
        :return:distance--float
        """
        pa_x, pa_y, pa_z = point1
        pb_x, pb_y, pb_z = point2
        pc_x, pc_y, pc_z = point3
        vector_ba = (pa_x - pb_x, pa_y - pb_y, pa_z - pb_z)
        vector_bc = (pc_x - pb_x, pc_y - pb_y, pc_z - pb_z)
        ba_cross_bc = [vector_ba[1] * vector_bc[2] - vector_ba[2] * vector_bc[1],
                       vector_ba[2] * vector_bc[0] - vector_ba[0] * vector_bc[2],
                       vector_ba[0] * vector_bc[1] - vector_ba[1] * vector_bc[0]]
        modulus_bc = math.sqrt(reduce(lambda x, y: x + y, map(lambda x: x ** 2, vector_bc)))
        modulus_ba_cross_bc = math.sqrt(reduce(lambda x, y: x + y, map(lambda x: x ** 2, ba_cross_bc)))
        return modulus_ba_cross_bc / modulus_bc

    @staticmethod
    def get_unique_index_group(low=0, high=5, n=3):
        """
        Get n indexs from low to high,if keep default,it may like return [1,4,2] eg.
        :param low:
        :param high:
        :param n:
        :return:index group
        """
        index_group = []
        while 1:
            index_group.append(np.random.randint(low, high))
            if len(set(index_group)) == n:
                return list(set(index_group))

    @staticmethod
    def get_multi_xyz_by_single_gene(gene, point1, point2_index_group, nums):
        """
        Get mulit (x,y) by one gene code who has one interference point(point1) & three unique radar points(point2_index_group)
        :param gene:contain multi params which encode to be binary
        :param point1:interference point (x,y,z)
        :param point2_index_group:like (2, 1, 0) whose value must be unique
        :param nums:numbers of generate new (x,y,z)
        :return:
        """
        # gene only contain three params in single uav:[(z,v,alpha),....]
        half_params = Code.decode(gene)
        # complement full params to be [(x,y,z,v,alpha),....]
        params = [Utils.get_xy_by_2p_z(point1, RADAR_POINTS[point2_index_group[i]], half_params[i][0]) + half_params[i]
                  for i in range(len(half_params))]
        return Utils.generate_multi_new_xyz_by_multi_params(params, nums)

    @staticmethod
    def generate_multi_new_xyz_by_multi_params(params, nums):
        """

        :param params:[(x0,y0,z0,v0,alpha0),...]
        :param nums:
        :return:
        """
        return [Utils._generate_multi_new_xyz_by_single_param(param, nums) for param in params]

    @staticmethod
    def _generate_multi_new_xyz_by_single_param(param, nums):
        x, y, z, v, alpha = param
        x_increment = v * TIME_INTERVAL * math.cos(alpha)
        y_increment = v * TIME_INTERVAL * math.sin(alpha)
        return [(x + (i + 1) * x_increment, y + (i + 1) * y_increment, z) for i in range(nums)]

    @staticmethod
    def get_xy_by_2p_z(point1, point2, z):
        """
        Get x,y by two points and high that a line through p1 & p2
        :param point1:point1
        :param point2:point2
        :param z:high
        :return:[x_value,y_value]--[float,float]
        """
        x1, y1, z1 = point1
        x2, y2, z2 = point2
        r = (z - z1) / (z2 - z1)

        return [r * (x2 - x1) + x1, r * (y2 - y1) + y1]

    @staticmethod
    def get_ranges(p1_list=RADAR_POINTS, p2_list=FAKE_POINTS, z_range=Z_RANGE):
        """

        :param p1_list:
        :param p2_list:
        :param z_range:
        :return:{FAKE_POINT_index:{RADAR_POINT_index:[(x_range), (y_range)])},...}
        """
        return {j: {i: GetRange.get_range(p1_list[i], p2_list[j], z_range) for i in range(len(p1_list))}
                for j in range(len(p2_list))}

    @staticmethod
    def get_better_values(z_list, p1_list=RADAR_POINTS, p2=FAKE_POINTS[0]):
        """

        :param p1_list:
        :param p2_list:
        :param z_range:
        :return:{FAKE_POINT_index:{RADAR_POINT_index:[(x_range), (y_range)])},...}

        """

        return [[GetRange.get_better_value(p1, p2, z_value) for p1 in p1_list] for z_value in z_list]

    @staticmethod
    def get_range(p1, p2, z_range=Z_RANGE):
        """

        :param p1:
        :param p2:
        :param z_range:
        :return:[x_range,y_range]
        """
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        return [(x1 + (z_range[0] - z1) * (x2 - x1) / (z2 - z1), x1 + (z_range[1] - z1) * (x2 - x1) / (z2 - z1)), \
                (y1 + (z_range[0] - z1) * (y2 - y1) / (z2 - z1), y1 + (z_range[1] - z1) * (y2 - y1) / (z2 - z1))]

    @staticmethod
    def get_better_value(p1, p2, z_value, bais=0):
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        x_range = (
            x1 + (z_value - bais - z1) * (x2 - x1) / (z2 - z1), x1 + (z_value + bais - z1) * (x2 - x1) / (z2 - z1)
        )
        y_range = (
            y1 + (z_value - bais - z1) * (y2 - y1) / (z2 - z1), y1 + (z_value + bais - z1) * (y2 - y1) / (z2 - z1)
        )
        return [np.random.random() * (x_range[1] - x_range[0]) + x_range[0],
                np.random.random() * (y_range[1] - y_range[0]) + y_range[0]]


if __name__ == "__main__":
    x_y_range = {j: {i: GetRange.get_range(RADAR_POINTS[i], FAKE_POINTS[j]) for i in range(len(RADAR_POINTS))}
                 for j in range(len(FAKE_POINTS))}
    print(x_y_range)

    import itertools

    print(np.random.random_integers(0, 5, [5, 3]))
    print(list(itertools.combinations(range(5), 3)))
    print(np.random.random())
