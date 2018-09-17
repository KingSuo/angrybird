from copy import deepcopy

import pandas as pd

from initialize import Initialize
from mutate import Mutate
from crossover import Crossover
from fitness import Fitness
from select_gene import Select
from code import Code


class JustGo:
    def __init__(self):
        pass

    @staticmethod
    def go(n, size):
        gene_codes = Initialize.initialize(n, size)
        m_n_t_points = list(map(Fitness.generate_n_t_points, gene_codes))

        fitness_list = list(map(Fitness.fitness, m_n_t_points))
        sum_fitness_before = sum(fitness_list)
        times = 0
        threshold = 1000

        while abs(threshold) > 0.000001:
            if times > 0:
                sum_fitness_before = sum_fitness_after
            new_gene_codes = [gene_codes[fitness_list.index(i)] for i in sorted(fitness_list, reverse=True)[:2]]
            while len(new_gene_codes) < size:
                gene_codes_copy = deepcopy(gene_codes)
                index_1 = Select.select(fitness_list)
                index_2 = Select.select(fitness_list)
                gene_code1 = gene_codes_copy[index_1]
                gene_code2 = gene_codes_copy[index_2]
                if index_1 != index_2:
                    gene_code1, gene_code2 = Crossover.crossover([gene_code1, gene_code2])
                gene_code1 = Mutate.mutate(gene_code1)
                gene_code2 = Mutate.mutate(gene_code2)
                new_gene_codes.append(gene_code1)
                if len(new_gene_codes) == size:
                    break
                else:
                    new_gene_codes.append(gene_code2)

                del gene_codes_copy
            gene_codes = new_gene_codes
            m_n_t_points = list(map(Fitness.generate_n_t_points, new_gene_codes))
            fitness_list = list(map(Fitness.fitness, m_n_t_points))
            sum_fitness_after = sum(fitness_list)
            threshold = sum_fitness_after - sum_fitness_before
            times += 1
            print('times', times)
            print('threshold = ', threshold)
            print('sum_fitness_after = ', sum_fitness_after)

        print(gene_codes)
        a = gene_codes[fitness_list.index(max(fitness_list))]
        b = Code.decode(a)
        c = Fitness.generate_n_t_points(a)
        print(a)
        print(b)
        print(c)

        data = []
        for temp in c:
            t = []
            for point in temp:
                x, y, z = point
                t.append(x)
                t.append(y)
                t.append(z)
            data.append(t)
        data_df = pd.DataFrame(data)
        writer = pd.ExcelWriter('%s.xlsx' % str(n))
        data_df.to_excel(writer, 'page_1', float_format='%.5f')  # float_format 控制精度
        writer.save()
        pd.ExcelWriter.save()

        # print(m_n_t_points)
        # print(m_n_t_points[0])
        # print(m_n_t_points[0][0])
        # print(len(m_n_t_points))
        # print(len(m_n_t_points[0]))
        # print(len(m_n_t_points[0][0]))


if __name__ == "__main__":
    JustGo.go(4, 80)
