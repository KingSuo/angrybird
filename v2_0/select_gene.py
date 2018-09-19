import numpy as np


class Select:
    def __init__(self):
        pass

    @staticmethod
    def select_n(fitness_list, n):
        """
        :param fitness_list:适应度值列表
        :return:下标index
        """
        return (Select.select(fitness_list) for _ in range(n))

    @staticmethod
    def select(fitness_list):
        """
        :param fitness_list:适应度值列表
        :return:下标index
        """
        incremental_probability = [sum(fitness_list[0:i + 1]) / sum(fitness_list) for i in range(len(fitness_list))]
        p = np.random.rand()
        for i in range(len(incremental_probability)):
            if p <= incremental_probability[0]:
                return 0
            elif incremental_probability[i] < p <= incremental_probability[i + 1]:
                return i + 1


if __name__ == '__main__':
    print(Select.select([6, 3, 1, 0, 1120, 1000, 2, 3, 5]))
