from functools import reduce

import pandas as pd

from v2_0.const import FAKE_POINTS
from v2_0.initialize import Initialize
from v2_0.gene_utils import Utils
from v2_0.fitness import Fitness
from v2_0.select_gene import Select
from v2_0.crossover import Crossover
from v2_0.mutate import Mutate
from v2_0.coding import Code


class Just:

    @staticmethod
    def go(param):
        t_moment, m, n, max_iteration_times, threshold = param
        long_gene_codes, point2_index_group = Initialize.initialize(m, n)
        point1_list = FAKE_POINTS[t_moment:]
        multi_xyz = Utils.get_multi_xyz_by_multi_long_gene_index_groups(
            long_gene_codes, FAKE_POINTS[t_moment], point2_index_group, len(FAKE_POINTS) - t_moment)
        point2_lists_list = multi_xyz
        group_fitness_list = Fitness.get_group_fitness_list(point1_list, point2_lists_list)
        sum_fitness_before = sum(group_fitness_list)
        bais = 10000
        flag = max_iteration_times
        evolution_times = 0

        while abs(bais) >= threshold and evolution_times < max_iteration_times:
            print('evolution_times = ', evolution_times)
            print('sum_fitness = ', sum_fitness_before)
            print('sum group_fitness_list = ', sum(group_fitness_list))
            if flag > max_iteration_times:
                sum_fitness_before = sum_fitness_after
            new_long_gene_codes = [long_gene_codes[group_fitness_list.index(fitness)]
                                   for fitness in sorted(group_fitness_list, reverse=True)[:10]]
            index_list = map(lambda index1, index2: (index1, index2),
                             Select.select_n(group_fitness_list, (m - len(new_long_gene_codes)) // 2),
                             Select.select_n(group_fitness_list, (m - len(new_long_gene_codes)) // 2))
            selected_gene_codes = ([long_gene_codes[index_1], long_gene_codes[index_2]]
                                   for index_1, index_2 in index_list)
            crossed_gene_codes = map(Crossover.crossover, selected_gene_codes)
            mutated_crossed_gene_codes = map(Mutate.mutate,
                                             reduce(lambda gene_code_1, gene_code_2: gene_code_1 + gene_code_2,
                                                    crossed_gene_codes))
            long_gene_codes = new_long_gene_codes + list(mutated_crossed_gene_codes)

            multi_xyz = Utils.get_multi_xyz_by_multi_long_gene_index_groups(
                long_gene_codes, FAKE_POINTS[t_moment], point2_index_group, len(FAKE_POINTS) - t_moment)
            point2_lists_list = multi_xyz
            group_fitness_list = Fitness.get_group_fitness_list(point1_list, point2_lists_list)
            sum_fitness_after = sum(group_fitness_list)
            bais = sum_fitness_after - sum_fitness_before
            print('bais = ', bais)
            evolution_times += 1

        population_min_distance_and_group_by_multi_interfere_point_multi_uav = \
            Fitness.get_population_min_distance_and_group_by_multi_interfere_point_multi_uav_list(point1_list,
                                                                                                  point2_lists_list)
        print('min distance in each time with uav and radar:')
        print(population_min_distance_and_group_by_multi_interfere_point_multi_uav)
        print(population_min_distance_and_group_by_multi_interfere_point_multi_uav[0])
        print(len(population_min_distance_and_group_by_multi_interfere_point_multi_uav))
        print(len(population_min_distance_and_group_by_multi_interfere_point_multi_uav[0]))
        print(len(population_min_distance_and_group_by_multi_interfere_point_multi_uav[0][0]))

        # save to excel
        max_fitness_index = group_fitness_list.index(max(group_fitness_list))
        max_fitness_gene_code = long_gene_codes[max_fitness_index]

        print(max_fitness_gene_code)
        print(multi_xyz)
        print(multi_xyz[0])
        print(len(multi_xyz))
        print(len(multi_xyz[0]))
        data = []
        for temp in multi_xyz[max_fitness_index]:
            t = []
            for point in temp:
                x, y, z = point
                t.append(x)
                t.append(y)
                t.append(z + 2000)
            data.append(t)
        decode_gene_code = Code.long_decode(max_fitness_gene_code)

        data_df1 = pd.DataFrame(data)
        data_df2 = pd.DataFrame(population_min_distance_and_group_by_multi_interfere_point_multi_uav[max_fitness_index])
        data_df3 = pd.DataFrame(decode_gene_code)
        writer = pd.ExcelWriter('Time_%s_无人机航线.xlsx' % str(t_moment))
        data_df1.to_excel(writer, '无人机', float_format='%.5f')  # float_format 控制精度
        data_df2.to_excel(writer, 'uav_radar', float_format='%.5f')  # float_format 控制精度
        data_df3.to_excel(writer, 'uav_v_alpha', float_format='%.5f')  # float_format 控制精度

        writer.save()


if __name__ == "__main__":
    params = ((i, 80, 3, 200, 0.01) for i in range(len(FAKE_POINTS)))
    from multiprocessing.dummy import Pool as ThreadPool

    pool = ThreadPool()
    pool.map(Just.go, params)
    pool.close()
    pool.join()
