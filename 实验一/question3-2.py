def xor_two_strings(str1, str2):
    """对两个等长字符串进行逐字符异或运算并返回结果"""
    return ''.join(chr(ord(char1) ^ ord(char2)) for char1, char2 in zip(str1, str2))


if __name__ == '__main__':
    hex_str1 = '1c0111001f010100061a024b53535009181c'
    hex_str2 = '686974207468652062756c6c277320657965'

    # 将十六进制字符串转换为原始字节字符串
    raw_bytes1 = bytes.fromhex(hex_str1)
    raw_bytes2 = bytes.fromhex(hex_str2)

    # 对两个字节字符串进行异或操作
    xor_result = xor_two_strings(raw_bytes1.decode('latin1'), raw_bytes2.decode('latin1'))

    # 将异或结果转换回十六进制表示
    final_hex_result = xor_result.encode('latin1').hex()

    print(final_hex_result)
