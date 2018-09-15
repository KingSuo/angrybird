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
    (80000, 0, 0)
    (30000, 60000, 0)
    (55000, 110000, 0)
    (105000, 110000, 0)
    (130000, 60000, 0)
]


class Fitness:
    def __init__(self):
        pass

    @staticmethod
    def fitness(uav_points_list):
        """

        :param uav_points_list:ｎ组无人机产生的２０个点,len()= (n, 20)
        :return:适应度值
        """
        distances = [list(map(Fitness.distances, FAKE_POINTS, uav_points)) for uav_points in uav_points_list]

    @staticmethod
    def distances(fake_point, uav_point):
        """

        :param fake_point:
        :param uav_point:
        :return:
        """
        dis = []
        x0, y0, z0 = fake_point
        for radar_point in RADAR_POINTS:
            x1, y1, z1 = radar_point
            x2, y2, z2 = uav_point


if __name__ == "__main__":
    a = list(map(lambda x, y: x + y, [1, 2, 3], [1, 1, 1]))
    print(a)
    for i in a:
        print(i)

    for i in a:
        print(i)
        print('==========')
