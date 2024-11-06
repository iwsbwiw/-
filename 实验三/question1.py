from math import gcd


def is_valid_e(e, phi, p_minus_1, q_minus_1):
    """
    检查 e 是否满足以下条件：
    1. gcd(e, phi) == 1
    2. gcd(e - 1, p - 1) == 2
    3. gcd(e - 1, q - 1) == 2
    """
    return gcd(e, phi) == 1 and gcd(e - 1, p_minus_1) == 2 and gcd(e - 1, q_minus_1) == 2


def sum_valid_e_values(p, q):
    phi = (p - 1) * (q - 1)  # 计算 φ(n)
    e_sum = 0

    # 从 e = 3 开始，只考虑奇数的 e 值
    for e in range(3, phi, 2):
        if is_valid_e(e, phi, p - 1, q - 1):
            e_sum += e

    return e_sum


# 输入参数 p 和 q
p = 1009
q = 3643

# 计算结果
result = sum_valid_e_values(p, q)
print("The sum of valid e values is:", result)
