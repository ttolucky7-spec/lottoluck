import pandas as pd
import random
from collections import Counter

print("🔥 실행됨")
import warnings

warnings.simplefilter("ignore")


# -----------------------------
# 엑셀 데이터 불러오기
# -----------------------------
def load_excel_data(start, end):

    numbers = []

    # 엑셀 읽기
    df = pd.read_excel("lotto.xlsx")

    for _, row in df.iterrows():

        draw = int(row.iloc[1])  # 회차

        if start <= draw <= end:

            numbers.extend(
                [
                    int(row.iloc[2]),
                    int(row.iloc[3]),
                    int(row.iloc[4]),
                    int(row.iloc[5]),
                    int(row.iloc[6]),
                    int(row.iloc[7]),
                ]
            )

    return numbers


# -----------------------------
# 2. 회차 범위 데이터 수집
# -----------------------------


# -----------------------------
# 3. 빈도 분석
# -----------------------------
def analyze_frequency(numbers):
    freq = Counter(numbers)

    for i in range(1, 46):
        if i not in freq:
            freq[i] = 0

    return freq


# -----------------------------
# 홀짝 필터
# -----------------------------
def check_odd_even(numbers, odd_count, even_count):

    odd = 0
    even = 0

    for n in numbers:

        if n % 2 == 0:
            even += 1
        else:
            odd += 1

    return odd == odd_count and even == even_count


# -----------------------------
# 4. 구간 나누기 (동률 허용)
# -----------------------------
def split_groups(freq):
    sorted_nums = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    # 1구간 (상위)
    cut1 = sorted_nums[5][1]
    g1 = [num for num, cnt in sorted_nums if cnt >= cut1]

    # 3구간 (하위)
    cut3 = sorted_nums[-6][1]
    g3 = [num for num, cnt in sorted_nums if cnt <= cut3]

    # 2구간 (중간)
    g2 = [num for num, cnt in sorted_nums if num not in g1 and num not in g3]

    return g1, g2, g3


# -----------------------------
# 5. 사용자 선택 적용
# -----------------------------
def apply_user_pick(user_nums, g1, g2, g3):
    user_set = set(user_nums)

    g1 = [n for n in g1 if n not in user_set]
    g2 = [n for n in g2 if n not in user_set]
    g3 = [n for n in g3 if n not in user_set]

    return user_set, g1, g2, g3


# -----------------------------
# 6. 가중치 기반 자동 배분
# -----------------------------
def weighted_allocate(g1, g2, g3, total_pick):
    w1, w2, w3 = 0.7, 1.8, 0.7

    total = len(g1) * w1 + len(g2) * w2 + len(g3) * w3

    n1 = int((len(g1) * w1 / total) * total_pick)
    n2 = int((len(g2) * w2 / total) * total_pick)
    n3 = int((len(g3) * w3 / total) * total_pick)

    allocated = n1 + n2 + n3
    remain = total_pick - allocated

    groups = [("g1", len(g1)), ("g2", len(g2)), ("g3", len(g3))]
    groups.sort(key=lambda x: x[1], reverse=True)

    for i in range(remain):
        if groups[i % 3][0] == "g1":
            n1 += 1
        elif groups[i % 3][0] == "g2":
            n2 += 1
        else:
            n3 += 1

    return n1, n2, n3


# -----------------------------
# 연속 숫자 검사
# -----------------------------
def check_consecutive(numbers, max_consecutive):

    count = 1

    for i in range(len(numbers) - 1):

        if numbers[i] + 1 == numbers[i + 1]:

            count += 1

            if count > max_consecutive:

                return False

        else:

            count = 1

    return True


# -----------------------------

# 최종 번호 생성

# -----------------------------

def generate_weighted_numbers(
    user_numbers,
    odd_count,
    even_count,
    max_consecutive,
    exclude_numbers
):

    # 사용자 번호와 제외 번호 충돌 검사
    for num in user_numbers:

        if num in exclude_numbers:

            raise ValueError(
                f"{num}번은 포함 번호와 제외 번호에 동시에 설정되었습니다."
            )

    
    freq = analyze_frequency(numbers)

    g1, g2, g3 = split_groups(freq)

    attempt = 0

    while attempt < 1000:

        attempt += 1

        # 그룹 복사
        temp_g1 = g1.copy()
        temp_g2 = g2.copy()
        temp_g3 = g3.copy()

        # 유저 번호 적용
        user_set, temp_g1, temp_g2, temp_g3 = apply_user_pick(
            user_numbers,
            temp_g1,
            temp_g2,
            temp_g3
        )

        remain = 6 - len(user_set)

        n1, n2, n3 = weighted_allocate(
            temp_g1,
            temp_g2,
            temp_g3,
            remain
        )

        result = set(user_set)

        if temp_g1:
            result.update(random.sample(temp_g1, min(n1, len(temp_g1))))

        if temp_g2:
            result.update(random.sample(temp_g2, min(n2, len(temp_g2))))

        if temp_g3:
            result.update(random.sample(temp_g3, min(n3, len(temp_g3))))

        # 부족하면 랜덤 추가
        all_nums = list(range(1, 46))

        while len(result) < 6:

            num = random.randint(1, 45)

            # 제외 숫자면 다시 생성
            if num in exclude_numbers:

                continue

            result.add(num)

        result = sorted(result)

        # -----------------------------
        # 홀짝 필터
        # -----------------------------
        if odd_count is not None:

            if not check_odd_even(result, odd_count, even_count):

                continue

        # -----------------------------
        # 연속 숫자 필터
        # -----------------------------
        if max_consecutive is not None:

            if not check_consecutive(result, max_consecutive):

                continue

        return result

    raise ValueError("조건에 맞는 번호를 생성할 수 없습니다.")




# -----------------------------
# 완전 랜덤 번호 생성
# -----------------------------
def generate_random_numbers(
    user_numbers,
    odd_count,
    even_count,
    max_consecutive,
    exclude_numbers
):



    # 사용자 번호와 제외 번호 충돌 검사
    for num in user_numbers:

        if num in exclude_numbers:

            raise ValueError(
                f"{num}번은 포함 번호와 제외 번호에 동시에 설정되었습니다."
            )

    attempt = 0

    while attempt < 1000:

        attempt += 1

        result = set(user_numbers)

        while len(result) < 6:

            num = random.randint(1, 45)

            if num in exclude_numbers:

                continue

            result.add(num)

        result = sorted(result)

        # 홀짝 필터
        if odd_count is not None:

            if not check_odd_even(result, odd_count, even_count):

                continue

        # 연속 숫자 필터
        if max_consecutive is not None:

            if not check_consecutive(result, max_consecutive):

                continue

        return result

    raise ValueError("조건에 맞는 번호를 생성할 수 없습니다.")


