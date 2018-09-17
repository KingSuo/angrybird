import numpy as np

from initialize import SINGLE_LEN


class Crossover:
    @staticmethod
    def crossover(gene_list, extra=None):
        """
        :param gene_list:两个基因的二进制编码，string
        :param extra:保留参数，后期优化进化使用
        :return:交叉后的新的gene_list
        """
        t = len(gene_list[0]) // SINGLE_LEN
        for _ in range(t if t > 0 else 1):
            gene_list = Crossover._crossover(gene_list, extra)
        # father, mother = gene_list
        # index = np.random.randint(0, len(gene_list[0]))
        # gene_list = [father[:index] + mother[index:], mother[:index] + father[index:]]
        return gene_list

    @staticmethod
    def _crossover(gene_list, extra=None):
        """
        :param gene_list:两个基因的二进制编码，string
        :param extra:保留参数，后期优化进化使用
        :return:交叉后的新的gene_list
        """
        father, mother = gene_list
        index0 = index1 = 0
        while index0 == index1:
            index0 = np.random.randint(0, len(gene_list[0]))
            index1 = np.random.randint(0, len(gene_list[0]))
        start = index0 if index0 < index1 else index1
        end = index0 if index0 > index1 else index1
        return [father[:start] + mother[start:end] + father[end:], mother[:start] + father[start:end] + mother[end:]]


if __name__ == '__main__':
    gene_list = ['111000', '000111']
    print(gene_list)
    print(Crossover.crossover(gene_list))
