import random
from math import gcd
from sympy import mod_inverse, isprime


# 生成指定位数的大素数
def generate_large_prime(bits=16):
    while True:
        num = random.getrandbits(bits)
        if num % 2 == 0:
            num += 1  # 确保是奇数
        if isprime(num):  # 素数检验
            return num


# 生成密钥对
def generate_rsa_keys(bits=16):
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    while p == q:
        q = generate_large_prime(bits)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    # 选择一个与 φ(n) 互质的 e
    e = 3
    while gcd(e, phi_n) != 1:
        e += 2

    d = mod_inverse(e, phi_n)
    return (e, n), (d, n)


# 加密
def encrypt(message, pub_key):
    """使用公钥加密消息"""
    e, n = pub_key
    return [pow(ord(char), e, n) for char in message]


# 解密
def decrypt(ciphertext, priv_key):
    d, n = priv_key
    return ''.join(chr(pow(char, d, n)) for char in ciphertext)


# 测试函数
def rsa_test():
    pub_key, priv_key = generate_rsa_keys(bits=16)
    print("Public key:", pub_key)
    print("Private key:", priv_key)

    message = "我从来没有觉得学密码学开心过"
    # 加密消息
    encrypted_message = encrypt(message, pub_key)
    print("Ciphertext:", encrypted_message)

    # 解密消息
    decrypted_message = decrypt(encrypted_message, priv_key)
    print("Plaintext:", decrypted_message)


# 执行测试
rsa_test()
