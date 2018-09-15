from numpy import pi
import numpy as np

# 每个无人机的参数对应二进制长度之和
X_LEN = 17
Y_LEN = 17
Z_LEN = 9
V_LEN = 10
ALPHA_LEN = 15

SINGLE_LEN = 68

X_RANGE = [30000, 130000]
Y_RANGE = [0, 110000]
Z_RANGE = [2000, 2500]
V_RANGE = [2000, 3000]

# 0~31415
ALPHA_RANGE = [0, int(pi * (10 ** 4))]


class Initialize:
    def __init__(self):
        pass

    @staticmethod
    def initialize(n, size):
        gene_codes = []
        for i in range(size):
            data = (Initialize._create_single_binary() for _ in range(n))
            s = ""
            for j in data:
                s += j
            gene_codes.append(s)
        return gene_codes

    @staticmethod
    def _create_single_binary():
        data = ("0" if np.random.rand() > .5 else "1" for _ in range(SINGLE_LEN))
        s = ""
        for i in data:
            s += i
        return s


if __name__ == "__main__":
    data = Initialize.initialize(2, 3)
    print(data)
    print(data[0])

    from code import Code

    decode = Code.decode(data[0])
    print(decode)

    x, y, z, v, alpha = decode[0]
    encode = Code.encode(x, y, z, v, alpha)
    print(encode)
