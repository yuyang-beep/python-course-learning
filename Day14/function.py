"""
Day14 - 函数和模块
课程：Python-100-Days / Day14.函数和模块
"""

# ============================================================
# 一、为什么需要函数？—— 消灭重复代码
# ============================================================
# 想计算组合数C(5,3)，需要分别求5!、3!、(5-3)!，再做除法
# 三段"求阶乘"的代码逻辑完全一样，只是循环上限不同——典型的重复代码

m, n = 5, 3

fm = 1
for i in range(1, m + 1):
    fm *= i

fn = 1
for i in range(1, n + 1):
    fn *= i

fk = 1
for i in range(1, m - n + 1):
    fk *= i

print(fm // fn // fk)     # 10 —— C(5,3)组合数

# 代码能跑，但同样的逻辑抄了三遍。把这段逻辑装进一个"函数"里，
# 以后哪里要用阶乘，直接"调用"这个函数即可，不用再抄一遍循环


# ============================================================
# 二、定义函数 —— def
# ============================================================

def factorial(num):        # def + 函数名 + 括号里是参数（数学上称自变量）
    result = 1
    for i in range(1, num + 1):
        result *= i
    return result            # return 返回结果（因变量）；没有return则默认返回None

print(factorial(5))          # 120  —— 调用：函数名+括号+参数
print(factorial(3))          # 6
print(factorial(5) // factorial(3) // factorial(2))   # 10 —— 复用同一个函数，不用再写循环

# 阶乘这种常见功能，Python标准库math模块其实已经提供了，没必要自己重复造轮子
from math import factorial as fac2      # as：给导入的函数起别名，避免和上面自定义的factorial同名冲突
print(fac2(5))                # 120 —— 效果和自己写的factorial一样


# ============================================================
# 三、函数的参数
# ============================================================

# 3.1 位置参数——按顺序传，个数要对应
def make_judgement(a, b, c):
    """判断三条边能否构成三角形"""
    return a + b > c and b + c > a and a + c > b

print(make_judgement(3, 4, 5))     # True
print(make_judgement(1, 2, 9))     # False

# 3.2 关键字参数——按"参数名=值"传，顺序无所谓
print(make_judgement(b=4, c=5, a=3))   # True，效果和位置传参完全一样

# 3.3 参数默认值——调用时不传就用默认值；有默认值的参数必须放在没有默认值的参数后面
import random

def roll_dice(n=2):
    total = 0
    for _ in range(n):
        total += random.randrange(1, 7)
    return total

print(roll_dice())      # 摇2颗骰子（用默认值2）
print(roll_dice(3))     # 摇3颗骰子（传参覆盖默认值）

# 3.4 可变参数 *args——收集任意多个位置参数，打包成一个元组
def add(*args):
    total = 0
    for val in args:
        total += val
    return total

print(add())               # 0    —— 一个参数都不传，args是空元组
print(add(1, 2, 3))        # 6
print(add(1, 2, 3, 4, 5))  # 15

# 3.5 可变关键字参数 **kwargs——收集任意多个关键字参数，打包成一个字典
def show_info(**kwargs):
    for key, value in kwargs.items():
        print(f'{key}: {value}')

show_info(name='小明', age=18)
# name: 小明
# age: 18


# ============================================================
# 四、用模块管理函数 —— import
# ============================================================
# 每个.py文件本身就是一个"模块"，不同模块里可以有同名函数；
# 靠import导入指定模块，用"模块名.函数名"这种完全限定名就能区分谁是谁，不会冲突

import math                     # 导入整个模块，用"模块名.函数名"调用
print(math.sqrt(16))            # 4.0

from math import pi             # 只导入需要的名字，用的时候不用加模块名前缀
print(pi)                       # 3.141592653589793

from math import sqrt as sq     # 导入并起别名，名字太长或怕和自己代码冲突时常用
print(sq(25))                   # 5.0


# ============================================================
# 五、内置函数 —— 不用import就能直接用
# ============================================================
# 之前几天已经在不知不觉中用过其中一些了：

print(len('hello'))         # 5     长度
print(max(3, 7, 2))          # 7     最大值
print(min([3, 7, 2]))        # 2     最小值（也支持直接传一个可迭代对象）
print(sum(range(1, 101)))    # 5050  求和
print(round(3.14159, 2))     # 3.14  四舍五入到指定小数位
print(type(3.14))            # <class 'float'>


# ============================================================
# 六、实战：把双色球选号功能封装成函数
# 之前几天每次生成号码都要重新写一遍随机选号的代码，
# 现在用函数封装起来，以后想生成号码，调用函数就行，不用再复制粘贴
# ============================================================

def draw_one(red_pool, blue_pool, red_count=6):
    """摇一注双色球号码，返回(红球元组, 蓝球)"""
    red = tuple(sorted(random.sample(red_pool, red_count)))
    blue = random.choice(blue_pool)
    return red, blue          # 同时"返回两个值"——本质是返回了一个元组，调用处再拆包


def draw_many(n, red_pool, blue_pool):
    """摇n注双色球号码，返回一个列表，列表的每一项是一注"""
    return [draw_one(red_pool, blue_pool) for _ in range(n)]


red_balls = list(range(1, 34))
blue_balls = list(range(1, 17))

n = int(input('\n生成几注双色球：'))
records = draw_many(n, red_balls, blue_balls)      # 一行代码搞定n注，逻辑全封装在函数里

for i, (red, blue) in enumerate(records, start=1):
    red_str = ' '.join(f'{b:02d}' for b in red)
    print(f'第{i}注：红球 [{red_str}]  蓝球 [{blue:02d}]')
