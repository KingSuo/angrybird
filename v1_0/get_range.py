from v1_0.const import Z_RANGE, RADAR_POINTS, FAKE_POINTS

import numpy as np


class GetRange:
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
