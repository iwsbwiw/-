import base64

def hex_to_base64(hex_string):
    """将十六进制字符串转换为 Base64 编码"""
    raw_bytes = bytes.fromhex(hex_string)
    # 将十六进制字符串转换为字节
    return base64.b64encode(raw_bytes).decode('utf-8')
    # 转换为 Base64 并解码为字符串

if __name__ == '__main__':
    hex_input = ("49276d206b696c6c696e6720796f757220627"
                 "261696e206c696b65206120706f69736f6e6f"
                 "7573206d757368726f6f6d")
    base64_output = hex_to_base64(hex_input)
    # 调用函数进行转换
    print(base64_output)
