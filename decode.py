from numpy import pi

# 每个无人机的参数对应二进制长度之和
x_len = 17
y_len = 17
z_len = 9
v_len = 10
alpha_len = 15

SINGLE_LEN = 68

x_range = [30000, 130000]
y_range = [0, 110000]
z_range = [2000, 2500]
v_range = [2000, 3000]
# 0~31415
alpha_range = [0, int(pi * (10 ** 4))]


class Code:
    def __init__(self):
        pass

    @staticmethod
    def decode(gene_code):
        """

        :param gene_code:二进制基因字符串
        :return:
        """
        if len(gene_code) % SINGLE_LEN != 0:
            print("Error for gene_code len: %d" % len(gene_code))
            return None
        else:
            data = []
            for i in range(0, len(gene_code), SINGLE_LEN):
                single = gene_code[i:SINGLE_LEN]
                x_binary = single[0:x_len]
                y_binary = single[x_len:x_len + y_len]
                z_binary = single[x_len + y_len:x_len + y_len + z_len]
                v_binary = single[x_len + y_len + z_len:x_len + y_len + z_len + v_len]
                alpha_binary = single[x_len + y_len + z_len + v_len:x_len + y_len + z_len + v_len + alpha_len]

                x = ((x_range[1] - x_range[0]) / (2 ** x_len -1)) * int(x_binary, 2) + x_range[0]
                y = ((y_range[1] - y_range[0]) / (2 ** y_len -1)) * int(y_binary, 2) + y_range[0]
                z = ((z_range[1] - z_range[0]) / (2 ** z_len -1)) * int(z_binary, 2) + z_range[0]
                v = ((v_range[1] - v_range[0]) / (2 ** v_len -1)) * int(v_binary, 2) + v_range[0]
                alpha = ((alpha_range[1] - alpha_range[0]) / (2 ** alpha_len -1)) * int(alpha_binary, 2) + alpha_range[0]
                data.append([x, y, z, v, alpha])
            return data

    @staticmethod
    def encode(x, y, z, v, alpha):
        x_binary = bin(((x - x_range[0]) * (2 ** x_len - 1)) // (x_range[1] - x_range[0])).split('0b')[-1]
        y_binary = bin(((y - y_range[0]) * (2 ** y_len - 1)) // (y_range[1] - y_range[0])).split('0b')[-1]
        z_binary = bin(((z - z_range[0]) * (2 ** z_len - 1)) // (z_range[1] - z_range[0])).split('0b')[-1]
        v_binary = bin(((v - v_range[0]) * (2 ** v_len - 1)) // (v_range[1] - v_range[0])).split('0b')[-1]

        alpha_binary = \
            bin(((alpha - alpha_range[0]) * (2 ** alpha_len - 1)) // (alpha_range[1] - alpha_range[0])).split('0b')[-1]

        x_prefix = "0" * (x_len - len(x_binary)) if len(x_binary) < x_len else ''
        y_prefix = "0" * (y_len - len(y_binary)) if len(y_binary) < y_len else ''
        z_prefix = "0" * (z_len - len(z_binary)) if len(z_binary) < z_len else ''
        v_prefix = "0" * (v_len - len(v_binary)) if len(v_binary) < v_len else ''
        alpha_prefix = "0" * (alpha_len - len(alpha_binary)) if len(alpha_binary) < alpha_len else ''

        x_binary = x_prefix + x_binary
        y_binary = y_prefix + y_binary
        z_binary = z_prefix + z_binary
        v_binary = v_prefix + v_binary
        alpha_binary = alpha_prefix + alpha_binary

        return x_binary + y_binary + z_binary + v_binary + alpha_binary


if __name__ == "__main__":
    encode_data = Code.encode(30000, 0, 2000, 2000, 0)
    print(encode_data)
    decode_data = Code.decode(encode_data)
    print(decode_data)

    encode_data = Code.encode(130000, 110000, 2500, 3000, 31415)
    print(encode_data)
    decode_data = Code.decode(encode_data)
    print(decode_data)
