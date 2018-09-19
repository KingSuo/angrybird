from functools import reduce
import numpy as np

from v2_0.const import RADAR_POINTS, Z_RANGE, V_RANGE, ALPHA_RANGE

from v2_0.coding import Code
from v2_0.gene_utils import Utils


class Initialize:
    def __init__(self):
        # self.x_y_range = GetRange.get_ranges()
        pass

    @staticmethod
    def initialize(m, n=3):
        """

        :param m:population size
        :param n:number of uav
        :return:array--shape:(m,n)
        """
        z_array = np.random.random_sample((m, n)) * (Z_RANGE[1] - Z_RANGE[0]) + Z_RANGE[0]
        v_array = np.random.random_sample((m, n)) * (V_RANGE[1] - V_RANGE[0]) + V_RANGE[0]
        alpha_array = np.random.random_sample((m, n)) * (ALPHA_RANGE[1] - ALPHA_RANGE[0]) + ALPHA_RANGE[0]
        radar_index_groups = np.array([Utils.get_unique_index_group(0, len(RADAR_POINTS)) for _ in range(m)])
        genes = [reduce(lambda gene1, gene2: gene1 + gene2, map(Code.encode, z_array[i], v_array[i], alpha_array[i]))
                 for i in range(len(z_array))]
        return genes, radar_index_groups


if __name__ == "__main__":
    print(Initialize.initialize(5, 3))
