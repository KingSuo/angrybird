import numpy as np

from const import SINGLE_LEN, X_LEN, Y_LEN, Z_LEN, V_LEN, ALPHA_LEN


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
        return gene_list

    @staticmethod
    def _crossover(gene_list, extra=None):
        """
        :param gene_list:两个基因的二进制编码，string
        :param extra:保留参数，后期优化进化使用
        :return:交叉后的新的gene_list
        """
        front = X_LEN + Y_LEN + Z_LEN
        father, mother = gene_list
        indexs = [(np.random.randint(front + i * SINGLE_LEN, front + V_LEN + ALPHA_LEN + i * SINGLE_LEN),
                   np.random.randint(front + i * SINGLE_LEN, front + V_LEN + ALPHA_LEN + i * SINGLE_LEN))
                  for i in range(len(gene_list[0]) // SINGLE_LEN)]
        for i in range(len(indexs)):
            start = min(indexs[i])
            end = max(indexs[i])
            temp = father[start:end]
            father = father[:start] + mother[start:end] + father[end:]
            mother = mother[:start] + temp + mother[end:]
        return [father, mother]


if __name__ == '__main__':
    gene_list = ['1111111011011111010001111100010011110101010001010010010011110011100001101101000011111000011110110000'
                 '0011011101100111111010101010010001010110110000100011110100111111100011101100101101110100011000000001'
                 '110010001110100100001011111101110011100001101000110100001100111110011000',
                 '1111111011011111010001111100010011110101010001010000010011010101100001101101000011111000011110110000'
                 '0011011101100111111000111010010001010101001000100000100100111111100011101000100101110001011000000001'
                 '110010001110100100001011111101110011100001001000111000101100111110000011']
    print(gene_list)
    print(Crossover.crossover(gene_list))
