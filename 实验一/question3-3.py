import re
def decrypt_hex_string(hex_str):
    """尝试使用异或逐字符解密十六进制字符串，返回解密后的字符串和对应密钥"""
    best_score = 0
    best_decrypted_str = ''
    best_key = ''

    # 遍历可能的密钥（0到128的ASCII字符）
    for potential_key in range(0, 129):
        decrypted_chars = []

        # 以两个字符为一组，解析十六进制字符串，并异或每个字符
        for byte_pair in re.findall('.{2}', hex_str):
            decrypted_chars.append(chr(potential_key ^ int(byte_pair, 16)))

        decrypted_str = ''.join(decrypted_chars)

        # 计算解密后的字符串中小写字母的数量，用于打分
        lowercase_count = sum(1 for char in decrypted_str if 'a' <= char <= 'z')

        # 如果当前密钥解密后的字符串得分更高，更新最佳解密结果
        if lowercase_count > best_score:
            best_score = lowercase_count
            best_decrypted_str = decrypted_str
            best_key = chr(potential_key)

    return best_key, best_decrypted_str

if __name__ == '__main__':
    hex_input = ("1b37373331363f78151b7f2b783431333d783"
                 "97828372d363c78373e783a393b3736")

    key, decrypted_message = decrypt_hex_string(hex_input)

    print(f"Key: {key}")
    print(f"Decrypted message: {decrypted_message}")
