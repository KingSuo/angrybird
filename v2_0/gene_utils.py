import math
from functools import reduce

import numpy as np

from v2_0.const import RADAR_POINTS, TIME_INTERVAL
from v2_0.coding import Code


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
        return modulus_ba_cross_bc / modulus_bc if modulus_bc else 0.000000000001

    @staticmethod
    def get_unique_index_group(low=0, high=5, n=3):
        """
        Get n indexs from low to high,if keep default,it may like return [1,4,2] eg.
        :param low:
        :param high:
        :param n:
        :return:index group--shape:(1,n)
        """
        index_group = []
        while 1:
            index_group.append(np.random.randint(low, high))
            if len(set(index_group)) == n:
                return list(set(index_group))

    @staticmethod
    def get_multi_xyz_by_multi_long_gene_index_groups(long_gene_codes, point1, point2_index_groups, nums):
        return [Utils.get_multi_xyz_by_single_long_gene(long_gene_codes[i], point1, point2_index_groups[i], nums)
                for i in range(len(long_gene_codes))]

    @staticmethod
    def get_multi_xyz_by_single_long_gene(long_gene_code, point1, point2_index_group, nums):
        """
        Get multi (x,y) by one gene code who has one interference point(point1) & three unique radar points(point2_index_group)
        :param long_gene_code:contain multi params which encode to be binary
        :param point1:interference point (x,y,z)
        :param point2_index_group:like (2, 1, 0) whose value must be unique
        :param nums:numbers of generate new (x,y,z)
        :return:[[(x,y,z), ...], [...], ...]--len()=3, shape()=(3,nums-1, 3)
        """
        # gene only contain three params in single uav:[(z,v,alpha),....]
        half_params = Code.long_decode(long_gene_code)
        # complement full params to be [(x,y,z,v,alpha),....]
        params = [Utils.get_xy_by_2p_z(point1, RADAR_POINTS[point2_index_group[i]], half_params[i][0]) + half_params[i]
                  for i in range(len(half_params))]
        return Utils.generate_multi_new_xyz_by_multi_params(params, nums)

    @staticmethod
    def generate_multi_new_xyz_by_multi_params(params, nums):
        """

        :param params:[(x0,y0,z0,v0,alpha0),...]--len()=3
        :param nums:
        :return:[[(x,y,z), ...], [...], ...]--len()=3, shape()=(3,nums-1, 3)
        """
        return [Utils.generate_multi_new_xyz_by_single_param(param, nums) for param in params]

    @staticmethod
    def generate_multi_new_xyz_by_single_param(param, nums):
        """

        :param param:param of (x, y, z, v, alpha)
        :param nums:num of residual locus points in different moments,eg:t0-->num=const.TIMES,ti-->num=const.TIMES-i
        :return:[(x,y,z), ...]--len()=nums-1, shape()=(1,nums-1, 3)
        """
        x, y, z, v, alpha = param
        x_increment = v * TIME_INTERVAL * math.cos(alpha)
        y_increment = v * TIME_INTERVAL * math.sin(alpha)
        return [(x + i * x_increment, y + i * y_increment, z) for i in range(nums)]

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


if __name__ == "__main__":
    from v2_0.const import FAKE_POINTS

    x, y = Utils.get_xy_by_2p_z(FAKE_POINTS[0], [80000, 0, 0], 2100)
    print(x, y)
    xyz_list = Utils.generate_multi_new_xyz_by_single_param((x, y, 2100, 40, 10), 20)
    print(xyz_list)
