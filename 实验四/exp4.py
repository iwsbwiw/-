import gmpy2
import time
from sympy.ntheory.modular import solve_congruence
from sympy import gcdex


# 数据提取部分
def extract_rsa_params(frame_data):
    N = int(frame_data[:256], 16)
    e = int(frame_data[256:512], 16)
    c = int(frame_data[512:], 16)
    return N, e, c


def process_frames_in_range(start, end):
    extracted_N, extracted_e, extracted_c = [], [], []
    for i in range(start, end + 1):
        file_path = f"Frame{i}"
        with open(file_path, 'r') as file:
            content = file.read().strip()
            frame_length = 768
            num_frames = len(content) // frame_length
            for j in range(num_frames):
                frame_data = content[j * frame_length: (j + 1) * frame_length]
                N, e, c = extract_rsa_params(frame_data)
                extracted_N.append(N)
                extracted_e.append(e)
                extracted_c.append(c)

    return extracted_N, extracted_e, extracted_c


# 从 Frame0 到 Frame20 的数据中提取模数N、公钥e和密文c
extracted_N, extracted_e, extracted_c = process_frames_in_range(0, 20)

# 打印提取的数据
for i in range(21):
    print(f"Frame{i} 提取的数据：\nN = {extracted_N[i]}\ne = {extracted_e[i]}\nc = {extracted_c[i]}")


# 攻击部分

# 将十六进制字符串转换为字符
def hex_to_char(hex_str):
    try:
        return bytes.fromhex(hex_str).decode('utf-8')
    except UnicodeDecodeError:
        return "Invalid Hex"


# 恢复明文
def recover_plaintext_from_factors(p, q, N, e, c):
    # 计算欧拉函数
    phi_N = (p - 1) * (q - 1)
    # 计算私钥d
    d = gmpy2.invert(e, phi_N)
    # 解密密文
    m = pow(c, d, N)
    # 将恢复的明文转换为十六进制字符串
    hex_plaintext = hex(m)[2:]  # 去掉 "0x" 前缀
    # 有效明文片段
    return hex_to_char(hex_plaintext[-16:])


# 低加密指数攻击
def low_exponent_attack(low_exponent_frames, e):
    a_list = []
    m_list = []
    # 组装同余方程
    for c, n in low_exponent_frames:
        a_list.append(c)
        m_list.append(n)
    try:
        # 使用中国剩余定理求解
        result = solve_congruence(*zip(a_list, m_list))
        x = result[0]  # m^e
    except Exception as ex:
        print(f"Error solving the congruence: {ex}")
        return None
    # 恢复明文
    try:
        m = gmpy2.iroot(x, e)[0]
    except Exception as ex:
        print(f"Error recovering plaintext: {ex}")
        return None
    return m


# 符合要求的数据
# 第一组数据：Frame7、Frame11、Frame15
low_exponent_frames_group_1 = [
    (extracted_c[7], extracted_N[7]),
    (extracted_c[11], extracted_N[11]),
    (extracted_c[15], extracted_N[15])
]

# 第二组数据：Frame3、Frame8、Frame12、Frame16、Frame20
low_exponent_frames_group_2 = [
    (extracted_c[3], extracted_N[3]),
    (extracted_c[8], extracted_N[8]),
    (extracted_c[12], extracted_N[12]),
    (extracted_c[16], extracted_N[16]),
    (extracted_c[20], extracted_N[20])
]

# 对两组数据进行低加密指数攻击
plaintext_group_1 = low_exponent_attack(low_exponent_frames_group_1, 3)
plaintext_group_2 = low_exponent_attack(low_exponent_frames_group_2, 5)

# 打印恢复的明文
hex_plaintext_group_1 = hex(plaintext_group_1)[2:]  # 去掉 "0x" 前缀
print("Recovered plaintext (Group 1):", hex_to_char(hex_plaintext_group_1[-16:]))

hex_plaintext_group_2 = hex(plaintext_group_2)[2:]  # 去掉 "0x" 前缀
print("Recovered plaintext (Group 2):", hex_to_char(hex_plaintext_group_2[-16:]))


# 公共模数攻击
def public_modulus_attack(frame1, frame2, N):
    c1, e1 = frame1
    c2, e2 = frame2
    # 计算扩展欧几里得
    x, y, g = gcdex(e1, e2)
    x, y = int(x), int(y)
    # 计算 c1^x * c2^y % N
    m = (pow(c1, x, N) * pow(c2, y, N)) % N
    return m


# 符合要求的数据：Frame0 和 Frame4
public_modulus_frames = [
    (extracted_c[0], extracted_e[0]),  # Frame0
    (extracted_c[4], extracted_e[4])  # Frame4
]

# 进行公共模数攻击
plaintext = public_modulus_attack(public_modulus_frames[0], public_modulus_frames[1], extracted_N[0])

# 打印恢复的明文
hex_plaintext = hex(plaintext)[2:]  # 去掉 "0x" 前缀
print("Recovered plaintext:", hex_to_char(hex_plaintext[-16:]))


# 模不互素攻击
def modulus_not_coprime_attack(modulus_not_coprime_frames):
    N1, c1, e1 = modulus_not_coprime_frames[0]
    N2, c2, e2 = modulus_not_coprime_frames[1]

    # 求最大公因数
    p = gmpy2.gcd(N1, N2)

    # 分解模数 n1 和 n2
    q1 = N1 // p
    q2 = N2 // p

    return p, q1, q2


# 符合要求的帧数据：Frame1 和 Frame18
modulus_not_coprime_frames = [
    (extracted_N[1], extracted_c[1], extracted_e[1]),  # Frame1
    (extracted_N[18], extracted_c[18], extracted_e[18])  # Frame18
]

# 执行模不互素攻击
p, q1, q2 = modulus_not_coprime_attack(modulus_not_coprime_frames)

# 打印分解出的模数和恢复的明文
print(f"Frame1 的模数 N 可分解为：\np = {p}\nq = {q1}")
print(f"Frame18 的模数 N 可分解为：\np = {p}\nq = {q2}")

# 恢复明文
plaintext1 = recover_plaintext_from_factors(p, q1, extracted_N[1], extracted_e[1], extracted_c[1])
print("Recovered plaintext (Frame1):", plaintext1)
plaintext18 = recover_plaintext_from_factors(p, q2, extracted_N[18], extracted_e[18], extracted_c[18])
print("Recovered plaintext (Frame18):", plaintext18)


# Fermat 分解攻击
def fermat_factorization_with_timeout(n, time_limit=10):
    start_time = time.time()  # 记录开始时间
    a = gmpy2.iroot(n, 2)[0] + 1  # 从大于 sqrt(n) 的整数开始
    while True:
        # 检查是否超时
        if time.time() - start_time > time_limit:
            print("费马分解超时")
            return None

        b2 = a * a - n
        if gmpy2.is_square(b2):
            b = gmpy2.iroot(b2, 2)[0]
            p = a - b
            q = a + b
            return p, q
        a += 1  # 否则继续增大 a


# 对每个数据进行Fermat分解攻击
for i, N in enumerate(extracted_N):
    result = fermat_factorization_with_timeout(N)
    if result:
        p, q = result
        print(f"Frame {i} 的模数N可分解为：\np = {p}\nq = {q}")
        print("Recovered plaintext:", recover_plaintext_from_factors(p, q, N, extracted_e[i], extracted_c[i]))
    else:
        print(f"Frame {i} 的模数N分解超时")


# Pollard p-1 攻击
def pollard_with_timeout(N, time_limit=10):
    start_time = time.time()  # 记录开始时间
    a = 2
    B = 2
    while True:
        # 检查是否超时
        if time.time() - start_time > time_limit:
            print("Pollard p-1 超时")
            return None

        a = gmpy2.powmod(a, B, N)  # 计算 a^B mod N
        res = gmpy2.gcd(a - 1, N)  # 计算 gcd(a - 1, N)

        if res != 1 and res != N:
            q = N // res
            return res, q  # 找到因子 p 和 q

        B += 1  # 增加 B 值继续尝试


# 对每个数据进行Pollard p-1攻击
for i, N in enumerate(extracted_N):
    result = pollard_with_timeout(N)
    if result:
        p, q = result
        print(f"Frame {i} 的模数N可分解为：\np = {p}\nq = {q}")
        print("Recovered plaintext:", recover_plaintext_from_factors(p, q, N, extracted_e[i], extracted_c[i]))
    else:
        print(f"Frame {i} 的模数N分解超时")
