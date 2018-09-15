from initialize import X_LEN, Y_LEN, Z_LEN, V_LEN, ALPHA_LEN
from initialize import X_RANGE, Y_RANGE, Z_RANGE, V_RANGE, ALPHA_RANGE, SINGLE_LEN


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
                single = gene_code[i:i + SINGLE_LEN]
                x_binary = single[0:X_LEN]
                y_binary = single[X_LEN:X_LEN + Y_LEN]
                z_binary = single[X_LEN + Y_LEN:X_LEN + Y_LEN + Z_LEN]
                v_binary = single[X_LEN + Y_LEN + Z_LEN:X_LEN + Y_LEN + Z_LEN + V_LEN]
                alpha_binary = single[X_LEN + Y_LEN + Z_LEN + V_LEN:X_LEN + Y_LEN + Z_LEN + V_LEN + ALPHA_LEN]

                x = ((X_RANGE[1] - X_RANGE[0]) / (2 ** X_LEN - 1)) * int(x_binary, 2) + X_RANGE[0]
                y = ((Y_RANGE[1] - Y_RANGE[0]) / (2 ** Y_LEN - 1)) * int(y_binary, 2) + Y_RANGE[0]
                z = ((Z_RANGE[1] - Z_RANGE[0]) / (2 ** Z_LEN - 1)) * int(z_binary, 2) + Z_RANGE[0]
                v = ((V_RANGE[1] - V_RANGE[0]) / (2 ** V_LEN - 1)) * int(v_binary, 2) + V_RANGE[0]
                alpha = ((ALPHA_RANGE[1] - ALPHA_RANGE[0]) / (2 ** ALPHA_LEN - 1)) * int(alpha_binary, 2) + ALPHA_RANGE[
                    0]
                data.append([x, y, z, v, alpha])
            return data

    @staticmethod
    def encode(x, y, z, v, alpha):
        x_binary = bin(((int(x) - X_RANGE[0]) * (2 ** X_LEN - 1)) // (X_RANGE[1] - X_RANGE[0])).split('0b')[-1]
        y_binary = bin(((int(y) - Y_RANGE[0]) * (2 ** Y_LEN - 1)) // (Y_RANGE[1] - Y_RANGE[0])).split('0b')[-1]
        z_binary = bin(((int(z) - Z_RANGE[0]) * (2 ** Z_LEN - 1)) // (Z_RANGE[1] - Z_RANGE[0])).split('0b')[-1]
        v_binary = bin(((int(v) - V_RANGE[0]) * (2 ** V_LEN - 1)) // (V_RANGE[1] - V_RANGE[0])).split('0b')[-1]

        alpha_binary = \
        bin(((int(alpha) - ALPHA_RANGE[0]) * (2 ** ALPHA_LEN - 1)) // (ALPHA_RANGE[1] - ALPHA_RANGE[0])).split('0b')[-1]

        x_prefix = "0" * (X_LEN - len(x_binary)) if len(x_binary) < X_LEN else ''
        y_prefix = "0" * (Y_LEN - len(y_binary)) if len(y_binary) < Y_LEN else ''
        z_prefix = "0" * (Z_LEN - len(z_binary)) if len(z_binary) < Z_LEN else ''
        v_prefix = "0" * (V_LEN - len(v_binary)) if len(v_binary) < V_LEN else ''
        alpha_prefix = "0" * (ALPHA_LEN - len(alpha_binary)) if len(alpha_binary) < ALPHA_LEN else ''

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
