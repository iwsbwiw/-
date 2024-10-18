import re
import base64

def english_score(sentence):
    """根据字符频率对句子进行打分，评估其是否为英文文本"""
    score = 0
    char_frequencies = {
        'a': 0.0651738, 'b': 0.0124248,
        'c': 0.0217339, 'd': 0.0349835,
        'e': 0.1041442, 'f': 0.0197881,
        'g': 0.0158610, 'h': 0.0492888,
        'i': 0.0558094, 'j': 0.0009033,
        'k': 0.0050529, 'l': 0.0331490,
        'm': 0.0202124, 'n': 0.0564513,
        'o': 0.0596302, 'p': 0.0137645,
        'q': 0.0008606, 'r': 0.0497563,
        's': 0.0515760, 't': 0.0729357,
        'u': 0.0225134, 'v': 0.0082903,
        'w': 0.0171272, 'x': 0.0013692,
        'y': 0.0145984, 'z': 0.0007836,
        ' ': 0.1918182
    }
    for char in sentence.lower():
        if char in char_frequencies:
            score += char_frequencies[char]
    return score


def hamming_distance(str1, str2):
    """计算两个字符串之间的汉明距离"""
    distance = 0
    for i in range(len(str1)):
        xor_result = ord(str1[i]) ^ ord(str2[i])
        while xor_result:
            if xor_result & 1:
                distance += 1
            xor_result >>= 1
    return distance


def find_best_key_char(hex_values):
    """找到最有可能的单字符密钥"""
    best_score = 0
    best_key = ''

    for key_candidate in range(256):
        decrypted_chars = []
        for hex_value in hex_values:
            decrypted_chars.append(chr(key_candidate ^ int(hex_value, 16)))
        decrypted_text = ''.join(decrypted_chars)
        score = english_score(decrypted_text)

        if score > best_score:
            best_score = score
            best_key = chr(key_candidate)

    return best_key


def main():
    with open("6.txt", "r") as file:
        # 解码并转换为字符串
        base64_content = [base64.b64decode(line.strip()).decode('latin1') for line in file.readlines()]
    decoded_content = "".join(base64_content)

    # 汉明距离计算，找到最优密钥长度
    key_length_candidates = []
    for key_size in range(1, 41):
        blocks = [decoded_content[i:i + key_size] for i in range(0, len(decoded_content), key_size)][:4]
        if len(blocks) == 4:
            distances = [
                hamming_distance(blocks[0], blocks[1]) / key_size,
                hamming_distance(blocks[1], blocks[2]) / key_size,
                hamming_distance(blocks[2], blocks[3]) / key_size,
                hamming_distance(blocks[0], blocks[2]) / key_size,
                hamming_distance(blocks[0], blocks[3]) / key_size,
                hamming_distance(blocks[1], blocks[3]) / key_size,
            ]
            avg_distance = sum(distances) / len(distances)
            key_length_candidates.append((key_size, avg_distance))

    key_length_candidates.sort(key=lambda x: x[1])

    # 打印最优密钥长度
    for candidate in key_length_candidates[:10]:
        print(f"Key length: {candidate[0]}, Avg Hamming distance: {candidate[1]}")

    # 转换为十六进制表示
    hex_content = decoded_content.encode('latin1').hex()

    # 分组
    blocks = [re.findall(r'(.{2})', hex_part) for hex_part in re.findall(r'(.{58})', hex_content)]

    # 找出每个块的密钥字符
    key = []
    for i in range(29):  # 假设密钥长度为29
        block_column = [block[i] for block in blocks if i < len(block)]
        key.append(find_best_key_char(block_column))

    key = ''.join(key)
    print(f"Derived key: {key}")

    # 使用密钥进行解密
    repeated_key = (key * ((len(decoded_content) // len(key)) + 1))[:len(decoded_content)]
    decrypted_message = ''.join(
        [chr(ord(decoded_content[i]) ^ ord(repeated_key[i])) for i in range(len(decoded_content))])

    print(f"Decrypted message:\n{decrypted_message}")

if __name__ == '__main__':
    main()
