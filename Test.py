# 星空印记 - 后端逻辑（无抽奖版）
# 路线 A：生日距离折扣 30% + 最短距离锁定
# 同一指纹永远得到同一天体

import math
from collections import OrderedDict

# 1. 天体指纹库（不变）
celestial_fp = {
    "昴宿星团":     {"season": "秋", "fp": ['F', 'C', 'W', 'E', 'A', 'S']},
    "蜂巢星团":     {"season": "春", "fp": ['W', 'C', 'S', 'F', 'E', 'A']},
    "毕宿星团":     {"season": "秋", "fp": ['E', 'C', 'W', 'F', 'S', 'A']},
    "双星团":      {"season": "春", "fp": ['A', 'S', 'C', 'F', 'W', 'E']},
    "猎户座大星云":  {"season": "冬", "fp": ['F', 'C', 'W', 'A', 'E', 'S']},
    "礁湖星云":    {"season": "夏", "fp": ['W', 'F', 'C', 'A', 'E', 'S']},
    "北美洲星云":  {"season": "夏", "fp": ['E', 'C', 'W', 'F', 'S', 'A']},
    "面纱星云":    {"season": "夏", "fp": ['W', 'A', 'S', 'C', 'F', 'E']},
    "哑铃星云":    {"season": "夏", "fp": ['A', 'S', 'W', 'F', 'C', 'E']},
    "环状星云":    {"season": "冬", "fp": ['S', 'E', 'W', 'C', 'F', 'A']},
    "武仙座球状星团": {"season": "春", "fp": ['C', 'E', 'W', 'F', 'S', 'A']},
    "奥米伽星团":  {"season": "春", "fp": ['C', 'W', 'F', 'S', 'E', 'A']},
}

# 2. 季节判定（不变）
def get_season(month):
    if 3 <= month <= 5: return "春"
    if 6 <= month <= 8: return "夏"
    if 9 <= month <= 11: return "秋"
    return "冬"

# 3. 问卷（不变）
def ask_question(text, opts):
    print(text)
    for k, v in opts.items(): print(f"  {k}. {v}")
    while True:
        ans = input("请选择（输入选项字母）：").strip().upper()
        if ans in opts: return ans

question_map = {
    "Q1": {
        "text": "Q1 你的能量核心更像？",
        "opts": OrderedDict([("A", "像年轻火焰，炽热而纯粹"), ("B", "像深海暗流，神秘且冷静"),
                            ("C", "像大地山川，包容而恒久"), ("D", "像风暴闪电，瞬息万变")]),
        "score": {"A": {'F': 3}, "B": {'W': 3}, "C": {'E': 3}, "D": {'A': 3}}
    },
    "Q2": {
        "text": "Q2 在世界中，你的存在方式？",
        "opts": OrderedDict([("A", "群星相拥，彼此映照"), ("B", "独自完美，闭环自洽"),
                            ("C", "双重交织，复杂多面"), ("D", "孕育新生，创造不止")]),
        "score": {"A": {'C': 3}, "B": {'S': 3}, "C": {'A': 3}, "D": {'F': 3}}
    },
    "Q3": {
        "text": "Q3 你对时间的感知？",
        "opts": OrderedDict([("A", "瞬间爆发，划过即逝"), ("B", "恒久稳定，亘古不变"),
                            ("C", "循环往复，周而复始"), ("D", "宏大轮廓，浩瀚无垠")]),
        "score": {"A": {'A': 3}, "B": {'E': 3}, "C": {'A': 3}, "D": {'C': 3}}
    },
}

# 4. 距离计算 + 生日折扣（无抽奖）
def main():
    print("=== 星空印记测试（宿命版 · 生日折扣 30%）===")
    month = int(input("请输入出生月份（1-12）："))
    season = get_season(month)
    print(f"你的出生季节：{season}\n")

    # 问卷得分
    dim_score = {'F': 0, 'W': 0, 'E': 0, 'A': 0, 'C': 0, 'S': 0}
    for q in question_map.values():
        ans = ask_question(q["text"], q["opts"])
        for d, v in q["score"][ans].items():
            dim_score[d] += v

    user_fp = sorted(dim_score, key=dim_score.get, reverse=True)
    print("\n你的维度得分：", {k: dim_score[k] for k in user_fp})
    print("指纹排序：", user_fp)

    # ① raw 距离
    raw_dist = {name: sum(abs(pos - user_fp.index(dim))
                         for pos, dim in enumerate(data["fp"]))
               for name, data in celestial_fp.items()}

    # ② 生日折扣 30%
    final_dist = {name: d * (1 - 0.30) if celestial_fp[name]["season"] == season else d
                 for name, d in raw_dist.items()}

    print("\n距离（含出生季节 30% 折扣）：", final_dist)

    # ③ 最短距离锁定
    result = min(final_dist.keys(), key=lambda name: final_dist[name])
    is_season = celestial_fp[result]["season"] == season

    print(f"\n✨ 你的星空印记：{result}")
    if is_season:
        print("🎉 出生季节已为你缩短 30% 距离，这是家乡的天空！")

if __name__ == "__main__":
    main()