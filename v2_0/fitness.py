import itertools
import numpy as np

from v2_0.gene_utils import Utils
from v2_0.const import RADAR_POINTS, FAKE_POINTS, MIN_RADAR_NUMS


class Fitness:
    def __init__(self):
        pass

    @staticmethod
    def fitness(uav_points_list, a=1000):
        pass

    @staticmethod
    def get_sum_group_fitness(point1_list, point2_lists_list):
        return sum(Fitness.get_group_fitness_list(point1_list, point2_lists_list))

    @staticmethod
    def get_group_fitness_list(point1_list, point2_lists_list):
        return [np.exp(-0.00001 * sum(map(lambda x: x[0], i)))
                for i in Fitness.get_population_min_distance_and_group_by_multi_interfere_point_multi_uav(
                point1_list, point2_lists_list)]

    @staticmethod
    def get_population_min_distance_and_group_by_multi_interfere_point_multi_uav(point1_list, point2_lists_list):
        return [Fitness.get_min_sum_distance_and_group_by_multi_interfere_point_multi_uav(
            point1_list, point2_lists) for point2_lists in point2_lists_list]

    @staticmethod
    def get_population_min_distance_and_group_by_multi_interfere_point_multi_uav_list(point1_list, point2_lists_list):
        return [list(Fitness.get_min_sum_distance_and_group_by_multi_interfere_point_multi_uav(
            point1_list, point2_lists)) for point2_lists in point2_lists_list]

    @staticmethod
    def get_min_sum_distance_and_group_by_multi_interfere_point_multi_uav(point1_list, point2_lists):
        """

        :param point1_list:
        :param point2_lists:Must ensure the len(point1_list)==len(point2_lists),
                            and shape(point2_lists) = (len(point1_list), 3, 3)
        :return:
        """
        return map(Fitness.get_min_sum_distance_and_group_by_single_interfere_point_multi_uav,
                   point1_list, Fitness.reshape_point_list(point2_lists))

    @staticmethod
    def get_min_sum_distance_and_group_by_single_interfere_point_multi_uav(point1, point2_list):
        return Fitness.get_min_sum_distance_and_group_by_multi_distances(
            Fitness.get_multi_distances_with_multi_uav_multi_radar_by_3points(point1, point2_list)
        )

    @staticmethod
    def get_min_sum_distance_and_group_by_multi_distances(multi_distances):
        # Make a mark for all distance, i represents which uav and j represents which radar
        mark_distance = {}
        # len(multi_distances) = 3
        for i in range(len(multi_distances)):
            # len(multi_distances[i]) = 5
            for j in range(len(multi_distances[i])):
                mark_distance[multi_distances[i][j]] = (i, j)
        combinations_sorted = sorted(itertools.combinations(mark_distance, MIN_RADAR_NUMS), key=lambda x: sum(x))
        for combination in combinations_sorted:
            d1, d2, d3 = combination
            if mark_distance[d1][0] != mark_distance[d2][0] and \
                    mark_distance[d1][0] != mark_distance[d3][0] and \
                    mark_distance[d2][0] != mark_distance[d3][0] and \
                    mark_distance[d1][1] != mark_distance[d2][1] and \
                    mark_distance[d1][1] != mark_distance[d3][1] and \
                    mark_distance[d2][1] != mark_distance[d3][1]:
                return sum(combination) / len(combination), \
                       [mark_distance[d1], mark_distance[d2], mark_distance[d3]]

    @staticmethod
    def get_multi_distances_with_multi_uav_multi_radar_by_3points(point1, point2_list, point3_list=RADAR_POINTS):
        return [Fitness.get_multi_distance_with_single_uav_multi_radar_by_3points(point1, point2, point3_list)
                for point2 in point2_list]

    @staticmethod
    def get_multi_distance_with_single_uav_multi_radar_by_3points(point1, point2, point3_list=RADAR_POINTS):
        return [Utils.get_distance_by_3points(point1, point2, point3_list[i]) for i in range(len(point3_list))]

    @staticmethod
    def reshape_point_list(point_list):
        return ([[point_list[i][j][k] for k in range(len(point_list[0][0]))]
                 for i in range(len(point_list))] for j in range(len(point_list[0])))


if __name__ == "__main__":
    x, y = Utils.get_xy_by_2p_z(FAKE_POINTS[0], RADAR_POINTS[1], 2100)
    print(x, y)

    # Test get_multi_distance_with_single_uav_multi_radar_by_3points()
    multi_distance = Fitness.get_multi_distance_with_single_uav_multi_radar_by_3points(
        FAKE_POINTS[0], [x, y, 2100]
    )
    print(multi_distance)
    print('===Test get_multi_distance_with_single_uav_multi_radar_by_3points()END===\n')

    # Test get_multi_distances_with_multi_uav_multi_radar_by_3points()
    z0 = 2100
    z1 = 2020
    z2 = 2400
    x0, y0 = Utils.get_xy_by_2p_z(FAKE_POINTS[0], RADAR_POINTS[0], z0)
    x1, y1 = Utils.get_xy_by_2p_z(FAKE_POINTS[0], RADAR_POINTS[1], z1)
    x2, y2 = Utils.get_xy_by_2p_z(FAKE_POINTS[0], RADAR_POINTS[2], z2)
    point2_list = [[x0, y0, z0], [x1, y1, z1], [x2, y2, z2]]

    multi_distances = Fitness.get_multi_distances_with_multi_uav_multi_radar_by_3points(FAKE_POINTS[0], point2_list)
    print(multi_distances)
    print('===Test get_multi_distances_with_multi_uav_multi_radar_by_3points()END===\n')

    # Test get_min_sum_distance_and_group()
    min_sum_distance_and_group = Fitness.get_min_sum_distance_and_group_by_multi_distances(multi_distances)
    print(min_sum_distance_and_group)
    print('===Test get_min_sum_distance_and_group()END===\n')

    # Test get_min_sum_distance_and_group_by_single_interfere_point_multi_uav()
    print(Fitness.get_min_sum_distance_and_group_by_single_interfere_point_multi_uav(FAKE_POINTS[0], point2_list))

    print('===Test get_min_sum_distance_and_group_by_single_interfere_point_multi_uav()END===\n')

    # Test get_min_sum_distance_and_group_by_multi_interfere_point_multi_uav()
    v0 = 40
    v1 = 45
    v2 = 38
    v = [v0, v1, v2]
    alpha0 = 100
    alpha1 = 70
    alpha2 = 230
    alpha = [alpha0, alpha1, alpha2]
    point1_list = FAKE_POINTS[1:]
    point2_lists = Utils.generate_multi_new_xyz_by_multi_params(
        map(lambda i, j, k: i + [j] + [k], point2_list, v, alpha), 20)
    min_sum_distance_list = list(Fitness.get_min_sum_distance_and_group_by_multi_interfere_point_multi_uav(
        point1_list, point2_lists
    ))
    print(min_sum_distance_list)
    print(len(min_sum_distance_list))

    print('===Test get_min_sum_distance_and_group_by_multi_interfere_point_multi_uav() END===\n')
