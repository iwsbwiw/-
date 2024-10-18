import hashlib
import itertools
import datetime

# 开始计时
start_time = datetime.datetime.now()

# 目标哈希值
target_hash = "67ae1a64661ac8b4494666f58c4822408dd0a3e4"

# 字符串选项
char_options = [
    ['Q', 'q'], ['W', 'w'], ['%', '5'], ['8', '('],
    ['=', '0'], ['I', 'i'], ['*', '+'], ['n', 'N']
]

# SHA1 加密函数
def sha1_encrypt(input_str):
    sha = hashlib.sha1(input_str.encode('utf-8'))
    return sha.hexdigest()

# 初始化候选字符串
candidate_str = ["0"] * 8

# 暴力破解
for a in range(2):
    candidate_str[0] = char_options[0][a]
    for b in range(2):
        candidate_str[1] = char_options[1][b]
        for c in range(2):
            candidate_str[2] = char_options[2][c]
            for d in range(2):
                candidate_str[3] = char_options[3][d]
                for e in range(2):
                    candidate_str[4] = char_options[4][e]
                    for f in range(2):
                        candidate_str[5] = char_options[5][f]
                        for g in range(2):
                            candidate_str[6] = char_options[6][g]
                            for h in range(2):
                                candidate_str[7] = char_options[7][h]
                                base_str = "".join(candidate_str)

                                # 生成所有可能的排列
                                for permutation in itertools.permutations(base_str, 8):
                                    test_str = "".join(permutation)
                                    hashed_str = sha1_encrypt(test_str)

                                    # 如果哈希匹配，输出结果并结束
                                    if hashed_str == target_hash:
                                        print(f"匹配的字符串: {test_str}")
                                        end_time = datetime.datetime.now()
                                        print(f"耗时: {(end_time - start_time).seconds} 秒")
                                        exit(0)
