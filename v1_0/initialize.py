from functools import reduce
import numpy as np

from v1_0.const import RADAR_POINTS, Z_RANGE, V_RANGE, SINGLE_LEN, ALPHA_RANGE

from v1_0.code import Code


class Initialize:
    def __init__(self):
        # self.x_y_range = GetRange.get_ranges()
        pass

    @staticmethod
    def initialize(n, size):
        return [reduce(lambda x, y: x + y, (Initialize._create_single_binary() for _ in range(n))) for _ in range(size)]

    @staticmethod
    def better_initialize(n, size):
        from v1_0.get_range import GetRange
        z_array = np.random.random_sample([size, n]) * (Z_RANGE[1] - Z_RANGE[0]) + Z_RANGE[0]
        xy_list_value = [GetRange.get_better_values(z_list) for z_list in z_array]
        radar_index = [Initialize._get_unique_index_group(0, len(RADAR_POINTS), n) for _ in range(size)]
        f1 = lambda x, y: x[y]
        xy_value = map(lambda x, y: map(f1, x, y), xy_list_value, radar_index)
        f2 = lambda xy, z: xy + [z] + \
                           [np.random.random() * (V_RANGE[1] - V_RANGE[0]) + V_RANGE[0],
                            np.random.random() * (ALPHA_RANGE[1] - ALPHA_RANGE[0]) + ALPHA_RANGE[0]]
        xyzvalpha = map(lambda xy, z: map(f2, xy, z), xy_value, z_array)
        f3 = lambda x: Code.encode(x[0], x[1], x[2], x[3], x[4])
        xyzvalpha_binary = list(map(lambda y: list(map(f3, y)), xyzvalpha))
        f4 = lambda x: reduce(lambda i, j: i + j, x)
        multi_xyzvalpha_binary = list(map(f4, xyzvalpha_binary))

        return multi_xyzvalpha_binary

    @staticmethod
    def _get_unique_index_group(low, high, n=3):
        index_group = []
        while 1:
            index_group.append(np.random.randint(low, high))
            if len(set(index_group)) == 3:
                index_group = list(set(index_group))
            if len(index_group) == n:
                return index_group

    @staticmethod
    def _create_single_binary():
        return reduce(lambda x, y: x + y, ("0" if np.random.rand() > .5 else "1" for _ in range(SINGLE_LEN)))

    @staticmethod
    def _create_single_better_binary(x_value, y_value, z_value, v_value, alpha_value):
        return Code.encode(x_value, y_value, z_value, v_value, alpha_value)


if __name__ == "__main__":
    data = Initialize.initialize(2, 3)
    print(data)
    print(data[0])

    decode = Code.decode(data[0])
    print(decode)

    x, y, z, v, alpha = decode[0]
    encode = Code.encode(x, y, z, v, alpha)
    print(encode)

    z = np.random.random_sample([3, 5]) * 500 + 2000
    print(z)
    print(np.random.random())
    print(np.random.random())
    print(np.random.random())
    print(np.random.random())

    xy_range = Initialize.better_initialize(2, 100)
    print(xy_range)
    print(xy_range[0])
    print(xy_range[0][0])
    print(len(xy_range))
    print(len(xy_range[0]))
    print(len(xy_range[0][0]))

    a = [1, 2]
    b = [2, 3]
    print(a + b)
    print(a.append(b))
