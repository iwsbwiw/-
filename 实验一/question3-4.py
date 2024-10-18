import re

def decrypt_hex_line(hex_line):
    """对十六进制字符串进行异或解密，返回解密后的字符串、密钥和得分"""
    best_score = 0
    best_decrypted_str = ''
    best_key = ''

    # 尝试使用不同的密钥进行异或解密
    for potential_key in range(0, 129):
        decrypted_chars = []

        # 以两个字符为一组，解析十六进制字符串，并异或每个字符
        for byte_pair in re.findall('.{2}', hex_line):
            decrypted_chars.append(chr(potential_key ^ int(byte_pair, 16)))

        decrypted_str = ''.join(decrypted_chars)

        # 计算解密后的字符串中字母和空格的数量，用于打分
        score = len(re.findall(r'[a-zA-Z ]', decrypted_str))

        # 如果当前密钥解密后的字符串得分更高，更新最佳结果
        if score > best_score:
            best_score = score
            best_decrypted_str = decrypted_str
            best_key = chr(potential_key)

    return best_key, best_decrypted_str, best_score

if __name__ == '__main__':
    # 读取文件中的每一行，并去掉换行符
    with open("4.txt", "r") as file:
        lines = [line.strip() for line in file.readlines()]

    overall_best_score = 0
    overall_best_line = ''
    overall_best_decrypted_str = ''
    overall_best_key = ''

    # 遍历文件中的每一行，逐行解密
    for hex_line in lines:
        key, decrypted_str, score = decrypt_hex_line(hex_line)

        # 如果当前行的解密得分更高，更新最佳解密结果
        if score > overall_best_score:
            overall_best_score = score
            overall_best_line = hex_line
            overall_best_decrypted_str = decrypted_str
            overall_best_key = key

    # 输出解密结果
    print(f"Original hex line: {overall_best_line}")
    print(f"Key: {overall_best_key}")
    print(f"Decrypted message: {overall_best_decrypted_str}")
