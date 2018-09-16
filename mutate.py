import numpy as np
from initialize import SINGLE_LEN


class Mutate:
    def __init__(self):
        pass

    @staticmethod
    def mutate(gene, extra=None):
        """
        :param gene:单个基因
        :param extra:
        :return:
        """
        t = len(gene) // SINGLE_LEN
        for _ in range(t if t > 0 else 1):
            gene = Mutate._mutate(gene)

        return gene

    @staticmethod
    def _mutate(gene):
        index = np.random.randint(0, len(gene))
        change = '0' if gene[index] == '1' else '1'
        return gene[:index] + change + gene[index + 1:]


if __name__ == '__main__':
    gene = '11111110110111110100011111000100111101010100010100100100111100111000011011010000111110000111101100000011' \
           '01110110011111101010101001000101011011000010000010010011111110001110110010110111010001100000000111001000' \
           '1110100100001011111101110011100001101000110100001100111110000000'
    print(gene)
    print(Mutate.mutate(gene))
