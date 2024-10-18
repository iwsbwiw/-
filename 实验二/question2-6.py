import base64
import os
import random
from Crypto.Cipher import AES
from Crypto.Util import Padding
import string

# 随机生成一个前缀长度
SUPER_SECRET_PREFIX_LENGTH = random.randint(0, 64)


# 加密 Oracle，使用随机密钥、随机前缀和 ECB 模式加密
def encryption_oracle(input_data: bytes) -> bytes:
    key = os.urandom(16)  # 生成随机密钥
    random_prefix = os.urandom(SUPER_SECRET_PREFIX_LENGTH)  # 生成随机前缀
    secret_suffix = base64.b64decode("""
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK""")  # 固定的 Base64 编码的密文后缀
    plaintext = random_prefix + input_data + secret_suffix  # 构造明文
    padded_plaintext = Padding.pad(plaintext, 16)  # 对明文进行填充
    cipher = AES.new(key, AES.MODE_ECB)  # 使用 ECB 模式创建加密器
    return cipher.encrypt(padded_plaintext)  # 返回加密后的密文


# 计算未知字符串长度，偏移量和填充长度
def get_unknown_length() -> tuple[int, int, int]:
    initial_length = len(encryption_oracle(b""))
    unknown_length = initial_length
    assert unknown_length % 16 == 0  # 确保是 16 字节的倍数

    # 通过逐渐增加输入长度，确定未知明文的真实长度
    for i in range(16):
        if len(encryption_oracle(b"A" * i)) != initial_length:
            unknown_length = initial_length - i
            break

    prefix_padding_length = 0
    while True:
        prefix_padding_length += 1
        encrypted_data = encryption_oracle(b"A" * prefix_padding_length)
        blocks = [encrypted_data[i: i + 16] for i in range(0, len(encrypted_data), 16)]
        # 通过检测重复块，找到前缀的实际长度
        for j in range(len(blocks) - 1):
            if blocks[j] == blocks[j + 1]:
                return unknown_length - j * 16 + prefix_padding_length % 16, j * 16, prefix_padding_length % 16


# 计算出未知字符串的长度、偏移和填充
unknown_length, prefix_offset, left_padding_len = get_unknown_length()
left_padding = b"\x00" * left_padding_len

# 可打印的字符空间
printable_characters = string.printable.encode()


# 搜索未知明文
def search_unknown_plaintext(known_plaintext: bytes) -> bool:
    while True:
        # 取最后 15 字节的已知明文，补齐到 15 字节
        partial_known = known_plaintext[-15:]
        partial_known = b"\x00" * (15 - len(partial_known)) + partial_known

        # 尝试所有可打印字符，寻找碰撞
        matched_chars = []
        for char in printable_characters:
            # 构造 Oracle 输入，填充到合适的长度
            oracle_input = left_padding + partial_known + bytes([char]) + b"\x00" * (15 - len(known_plaintext) % 16)
            encrypted_output = encryption_oracle(oracle_input)[prefix_offset:]
            if encrypted_output[15] == encrypted_output[(len(known_plaintext) // 16) * 16 + 31]:
                matched_chars.append(char)

        if len(matched_chars) == 1:
            # 找到唯一匹配字符，添加到已知明文中
            known_plaintext += bytes(matched_chars)
            print(known_plaintext)

            if len(known_plaintext) == unknown_length:  # 如果已知明文长度等于未知明文总长度，退出
                return True
            continue
        elif len(matched_chars) == 0:
            # 未找到匹配，搜索失败
            return False
        else:
            # 多个匹配，递归搜索
            for matched_char in matched_chars:
                if search_unknown_plaintext(known_plaintext + bytes([matched_char])):
                    return True


# 开始搜索未知明文
search_unknown_plaintext(b"")
