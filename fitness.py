from itertools import combinations
from math import sin, cos
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool as ProcessPool

from utils import Utils
from initialize import TIME_INTERVAL, TIMES
from code import Code

RADAR_1 = (80000, 0, 0)
RADAR_2 = (30000, 60000, 0)
RADAR_3 = (55000, 110000, 0)
RADAR_4 = (105000, 110000, 0)
RADAR_5 = (130000, 60000, 0)

# 第一题航线坐标(m)
FAKE_POINTS = [
    [60600, 69982, 7995],
    [61197, 69928, 7980],
    [61790, 69838, 7955],
    [62377, 69713, 7920],
    [62955, 69553, 7875],
    [63523, 69359, 7820],
    [64078, 69131, 7755],
    [64618, 68870, 7680],
    [65141, 68577, 7595],
    [65646, 68253, 7500],
    [66131, 67900, 7395],
    [66594, 67518, 7280],
    [67026, 67116, 7155],
    [67426, 66697, 7020],
    [67796, 66263, 6875],
    [68134, 65817, 6720],
    [68442, 65361, 6555],
    [68719, 64897, 6380],
    [68966, 64429, 6195],
    [69184, 63957, 6000],
]

RADAR_POINTS = [
    [80000, 0, 0],
    [30000, 60000, 0],
    [55000, 110000, 0],
    [105000, 110000, 0],
    [130000, 60000, 0],
]


class Fitness:
    def __init__(self):
        pass

    @staticmethod
    def fitness(uav_points_list, a=1000):
        """

        :param uav_points_list:ｎ组无人机产生的２０个点,len()= (n, 20)
                eg. uav_points_list = [
                                        [(x0,y0,z0), (x0,y0,z0), ..(x19,y19,z19)]_0,
                                        []_1,...,
                                        []_n-1
                                      ],ｎ即为无人机个数
        :return:适应度值
        """
        distances = [list(map(Fitness.distances, FAKE_POINTS, uav_points)) for uav_points in uav_points_list]

        t_ds = [[distances[n][t] for n in range(len(distances))] for t in range(len(distances[0]))]

        # n_t_ks ｎ表示ｎ架飞机，ｔ表示ｔ个时刻，ｋ表示ｋ个雷达, shape(n_t_ks)=(20,4)
        # [[(1, 0), (3, 4), (4, 3), (5242.194153377439, 4290.566586304617, 7554.080268124958)], [(0, 1), (4, 3), (6, 1), (7195.230361679737, 5161.329938602927, 6801.371035079191)],...]
        n_t_ks = list(map(Fitness._get_3_points, t_ds))
        # print(n_t_ks)
        fitness_values = [a / (sum(i[-1]) / len(i[-1])) for i in n_t_ks]
        fitness = sum(fitness_values) / len(fitness_values)

        # print(distances)
        # print(distances[0])
        # print(distances[0][0])
        # print(len(distances))
        # print(len(distances[0]))
        # print(len(distances[0][0]))
        # print(fitness_values)
        # print(min(fitness_values), max(fitness_values))

        # print(t_ds)
        # print(t_ds[0])
        # print(t_ds[0][0])
        # print(len(t_ds))
        # print(len(t_ds[0]))
        # print(len(t_ds[0][0]))
        return fitness

    @staticmethod
    def distances(fake_point, uav_point):
        """

        :param fake_point:
        :param uav_point:
        :return:
        """
        return [Utils.compute_min_distance(fake_point, radar_point, uav_point) for radar_point in RADAR_POINTS]

    @staticmethod
    def _get_3_points(n_5):
        """

        :param n_5:ｎ架飞机，５个距离(同一时刻同一个fake点对ｎ架飞机与５个雷达构成直线的距离)
        :return:来自３个不同飞机的同一时刻的坐标
        """
        # points_dict = {}
        # for i in range(len(n_5)):
        #     for j in range(len(n_5[i])):
        #         if n_5[i][j] not in points_dict.keys():
        #             points_dict[n_5[i][j]] = [i, j]
        #         else:
        #             print('WARING: %f existed in the points_dict!!!' % n_5[i][j])
        # t_i, t_j = points_dict[n_5[i][j]]

        points_dict = {n_5[i][j]: [i, j] for j in range(len(n_5[0])) for i in range(len(n_5))}
        combinations_list = combinations(points_dict, 3)
        combinations_list_sorted = sorted([(i, sum(i)) for i in combinations_list], key=lambda x: x[1])
        for i in combinations_list_sorted:
            point0_dis, point1_dis, point2_dis = i[0]
            i_0, j_0 = points_dict[point0_dis]
            i_1, j_1 = points_dict[point1_dis]
            i_2, j_2 = points_dict[point2_dis]
            if i_0 != i_1 != i_2 and j_0 != j_1 != j_2:
                return [(i_0, j_0), (i_1, j_1), (i_2, j_2), (point0_dis, point1_dis, point2_dis)]

    @staticmethod
    def generate_n_t_points(gene_code):
        """

        :param gene_code:单个基因二进制编码(保存ｎ架飞机的参数数据)
        :return:ｎ个无人机t个时刻的坐标
        """
        uav_params = Code.decode(gene_code)
        return list(map(Fitness._generate_t_points, uav_params))

    @staticmethod
    def _generate_t_points(uav_param):
        """

        :param uav_param:单个无人机的参数
        :return:该无人机t个时刻的坐标
        """
        x, y, z, v, alpha = uav_param
        return [
            (x + v * TIME_INTERVAL * t * cos(alpha / (10 ** 4)), y + v * TIME_INTERVAL * t * sin(alpha / (10 ** 4)), z)
            for t in range(TIMES)]


if __name__ == "__main__":
    # uav_point = [40000, 10000, 2100]
    # dis = Fitness.distances(FAKE_POINTS[0], uav_point)
    # print(dis)
    #
    # a = {11.1: 11, 12.0: 21, 13: 31, 1: 11, 2: 21, 3: 31, 4: 41}
    # plzh = list(combinations(a, 3))
    # plzh_l = [(i, sum(i)) for i in plzh]
    # print(sorted(plzh))
    # print(plzh_l)
    # print(sorted(plzh_l, key=lambda x: x[1]))

    from initialize import Initialize

    group = Initialize.initialize(20, 10)
    print(group)
    print(len(group))
    print(len(group[0]))

    uav_points_list = [[[j[0], j[1], j[2]] for j in i] for i in list(map(Code.decode, group))]
    print(uav_points_list)
    print(uav_points_list[0])
    print(len(uav_points_list))
    print(len(uav_points_list[0]))
    print("=" * 10)

    Fitness.fitness(uav_points_list)
# 0.1663817066213695
# 0.18428780906821607
