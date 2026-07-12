"""
Day07 - 分支和循环结构实战
课程：Python-100-Days / Day07.分支和循环结构实战
今天是纯实战：用前几天学的 if/for/while 解决5个经典问题
"""

# ============================================================
# 例子1：输出 100 以内的所有素数
# 素数 = 只能被 1 和自身整除的正整数
# ============================================================

print('=== 100以内的素数 ===')
for num in range(2, 100):
    is_prime = True
    for i in range(2, int(num ** 0.5) + 1):  # 只需检查到 √num
        if num % i == 0:
            is_prime = False
            break
    if is_prime:
        print(num, end=' ')
print()


# ============================================================
# 例子2：斐波那契数列前 20 个数
# 规律：前两个是1，之后每个 = 前两个之和
# 1, 1, 2, 3, 5, 8, 13, 21, 34 ...
# ============================================================

print('\n=== 斐波那契数列（前20个）===')
a, b = 0, 1
for _ in range(20):
    a, b = b, a + b   # 同时更新：a变成b，b变成a+b
    print(a, end=' ')
print()


# ============================================================
# 例子3：水仙花数（100~999 中满足 个位³+十位³+百位³ = 自身）
# 例：153 = 1³ + 5³ + 3³ = 1 + 125 + 27 = 153 ✅
# ============================================================

print('\n=== 水仙花数 ===')
for num in range(100, 1000):
    low  = num % 10        # 个位
    mid  = num // 10 % 10  # 十位
    high = num // 100      # 百位
    if num == low**3 + mid**3 + high**3:
        print(num, end=' ')
print()


# ============================================================
# 例子4：百钱百鸡
# 公鸡5元/只，母鸡3元/只，小鸡1元/3只
# 100元买100只，各买几只？
# ============================================================

print('\n=== 百钱百鸡 ===')
for x in range(0, 21):        # 公鸡最多买 100//5=20 只
    for y in range(0, 34):    # 母鸡最多买 100//3=33 只
        z = 100 - x - y       # 小鸡数量由总数决定
        if z % 3 == 0 and 5*x + 3*y + z//3 == 100:
            print(f'公鸡 {x} 只，母鸡 {y} 只，小鸡 {z} 只')


# ============================================================
# 例子5：CRAPS 花旗骰游戏（综合运用循环+分支+随机数）
# 规则：
#   第一次摇出 7 或 11 → 玩家胜
#   第一次摇出 2、3、12 → 庄家胜
#   其他点数 → 继续摇，摇出7庄家胜，摇出原点数玩家胜
# ============================================================

import random
print('\n=== CRAPS 花旗骰游戏 ===')
money = 1000

while money > 0:
    print(f'当前资产：{money} 元')
    while True:
        bet = int(input('请下注（输入金额）：'))
        if 0 < bet <= money:
            break
        print(f'下注金额需在 1 ~ {money} 之间')

    first = random.randrange(1, 7) + random.randrange(1, 7)
    print(f'第一次摇出：{first} 点')

    if first in (7, 11):
        print('玩家胜！\n')
        money += bet
    elif first in (2, 3, 12):
        print('庄家胜！\n')
        money -= bet
    else:
        while True:
            current = random.randrange(1, 7) + random.randrange(1, 7)
            print(f'摇出：{current} 点')
            if current == 7:
                print('庄家胜！\n')
                money -= bet
                break
            elif current == first:
                print('玩家胜！\n')
                money += bet
                break

    if money > 0:
        again = input('继续游戏？(y/n)：')
        if again.lower() != 'y':
            print(f'游戏结束，你离开时有 {money} 元。')
            break

if money <= 0:
    print('你破产了，游戏结束！')
