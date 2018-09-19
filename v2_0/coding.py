from v2_0.const import X_LEN, Y_LEN, Z_LEN, V_LEN, ALPHA_LEN, \
    X_RANGE, Y_RANGE, Z_RANGE, V_RANGE, SINGLE_LEN, ALPHA_RANGE


class Code:
    def __init__(self):
        pass

    @staticmethod
    def long_decodes(long_gene_codes):
        return map(Code.long_decode, long_gene_codes)

    @staticmethod
    def long_decode(long_gene_code):
        return [Code.decode(long_gene_code[i:i + SINGLE_LEN]) for i in range(0, len(long_gene_code), SINGLE_LEN)]

    @staticmethod
    def decode(gene_code):
        """

        :param gene_code:二进制基因字符串
        :return:
        """
        if len(gene_code) % SINGLE_LEN != 0:
            print(gene_code)
            print("Error for gene_code len: %d" % len(gene_code))
            return None
        else:
            data = []
            for i in range(0, len(gene_code), SINGLE_LEN):
                single = gene_code[i:i + SINGLE_LEN]
                z_binary = single[0:Z_LEN]
                v_binary = single[Z_LEN:Z_LEN + V_LEN]
                alpha_binary = single[Z_LEN + V_LEN:Z_LEN + V_LEN + ALPHA_LEN]

                z = ((Z_RANGE[1] - Z_RANGE[0]) / (2 ** Z_LEN - 1)) * int(z_binary, 2) + Z_RANGE[0]
                v = ((V_RANGE[1] - V_RANGE[0]) / (2 ** V_LEN - 1)) * int(v_binary, 2) + V_RANGE[0]
                alpha = ((ALPHA_RANGE[1] - ALPHA_RANGE[0]) / (2 ** ALPHA_LEN - 1)) * \
                        int(alpha_binary, 2) + ALPHA_RANGE[0]
                data.append(z)
                data.append(v)
                data.append(alpha)
            return data

    @staticmethod
    def encode(z, v, alpha):
        z_binary = bin(((int(z) - Z_RANGE[0]) * (2 ** Z_LEN - 1)) // (Z_RANGE[1] - Z_RANGE[0])).split('0b')[-1]
        v_binary = bin(((int(v) - V_RANGE[0]) * (2 ** V_LEN - 1)) // (V_RANGE[1] - V_RANGE[0])).split('0b')[-1]
        alpha_binary = bin(
            ((int(alpha) - ALPHA_RANGE[0]) * (2 ** ALPHA_LEN - 1)) // (ALPHA_RANGE[1] - ALPHA_RANGE[0])
        ).split('0b')[-1]

        z_prefix = "0" * (Z_LEN - len(z_binary)) if len(z_binary) < Z_LEN else ''
        v_prefix = "0" * (V_LEN - len(v_binary)) if len(v_binary) < V_LEN else ''
        alpha_prefix = "0" * (ALPHA_LEN - len(alpha_binary)) if len(alpha_binary) < ALPHA_LEN else ''

        z_binary = z_prefix + z_binary
        v_binary = v_prefix + v_binary
        alpha_binary = alpha_prefix + alpha_binary

        return z_binary + v_binary + alpha_binary


if __name__ == "__main__":
    encode_data = Code.encode(0, 33.3, 0)
    print(encode_data)
    decode_data = Code.decode(encode_data)
    print(decode_data)

    encode_data = Code.encode(500, 50, 628)
    print(encode_data)
    decode_data = Code.decode(encode_data)
    print(decode_data)

    print(Code.long_decode(encode_data * 3))
    print(len(Code.long_decode(encode_data * 3)[0]))

    print(list(Code.long_decodes([encode_data * 3, encode_data * 3, encode_data * 3, encode_data * 3])))
