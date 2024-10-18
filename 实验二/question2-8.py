import Crypto.Cipher.AES as AES
import Crypto.Util.Padding as padding
import os

# 加密密钥，16字节长度的随机密钥
key = b"\xc6\xfe\xe2/\x97r|/\xeaY\xc5C\xbfi\x99\x97"


def encrypt(user_data: bytes) -> bytes:
    # 对用户输入的字符串做 URL 编码处理
    safe_data = (
            b"comment1=cooking MCs;userdata="
            + user_data.replace(b";", b"%3B").replace(b"=", b"%3D")
            + b";comment2= like a pound of bacon"
    )
    # 使用随机生成的 16 字节 IV 和 CBC 模式对数据进行加密，并在前面填充 16 字节的 0
    cipher = AES.new(key, AES.MODE_CBC, os.urandom(16))
    encrypted = cipher.encrypt(padding.pad((b"\x00" * 16) + safe_data, 16))

    print(f"原始数据: {safe_data}")
    print(f"加密数据: {encrypted.hex()}\n")

    return encrypted


def decrypt(encrypted_data: bytes) -> dict:
    # 使用 CBC 模式解密数据，移除前面的 16 字节填充部分
    cipher = AES.new(key, AES.MODE_CBC, os.urandom(16))
    decrypted_data = padding.unpad(cipher.decrypt(encrypted_data), 16)[16:]

    print(f"解密后的数据: {decrypted_data}\n")

    # 将解密后的数据拆分为 key=value 的键值对，并返回字典
    return {
        (kv_pair := item.split(b"=", maxsplit=1))[0].decode(): kv_pair[1]
        for item in decrypted_data.split(b";")
    }


def is_admin(encrypted_data: bytes) -> bool:
    decrypted = decrypt(encrypted_data)
    is_admin = decrypted.get("admin") == b"true"
    print(f"管理员权限验证: {'是' if is_admin else '否'}\n")
    return is_admin


# 模拟攻击者尝试通过修改加密数据来构造 'admin=true'
pad_length = 18
user_input = b"A" * pad_length + b":admin<true"  # 用户输入伪造的 admin 字段

# 加密用户输入的数据
encrypted_message = bytearray(encrypt(user_input))

# 修改密文中的某些字节来尝试篡改解密后的内容
print(f"篡改前的加密数据: {encrypted_message.hex()}\n")
encrypted_message[pad_length + 30] ^= 1  # 通过异或操作修改密文中的第一个字节
encrypted_message[pad_length + 36] ^= 1  # 修改密文中的第二个字节
print(f"篡改后的加密数据: {encrypted_message.hex()}\n")

# 验证解密后是否成为了 admin=true
if is_admin(encrypted_message):
    print("成功获取管理员权限！")
else:
    print("管理员权限验证失败。")
