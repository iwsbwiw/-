def xor_with_repeating_key(key, text):
    """使用重复的密钥对文本进行异或加密"""
    key_length = len(key)
    encrypted_result = []

    # 逐字符与重复密钥异或
    for index, char in enumerate(text):
        key_char = key[index % key_length]  # 取当前字符对应的密钥字符
        encrypted_char = chr(ord(key_char) ^ ord(char))  # 异或操作
        encrypted_result.append(encrypted_char)

    return ''.join(encrypted_result)

def main():
    text = ("Burning 'em, if you ain't quick and"
            " nimble\nI go crazy when I hear a cymbal")
    key = 'ICE'

    # 执行加密并转换为十六进制表示
    encrypted_text = xor_with_repeating_key(key, text)
    hex_output = encrypted_text.encode('latin1').hex()
    print(hex_output)

if __name__ == '__main__':
    main()
