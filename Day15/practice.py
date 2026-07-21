"""
Day15 - 函数应用实战
课程：Python-100-Days / Day15.函数应用实战
"""
# 这节课不引入太多新语法，而是用5个实际例子，练习Day14学的def/参数/返回值，
# 顺带学几个实用小技巧：命名关键字参数、类型注解、函数互相调用、ANSI上色输出


# ============================================================
# 一、实战：随机验证码
# ============================================================
# 验证码由数字+英文大小写字母构成，长度可以通过参数指定

import random
import string

ALL_CHARS = string.digits + string.ascii_letters   # '0123456789' + 大小写字母，共62个字符


def generate_code(*, code_len=4):
    """生成指定长度的验证码"""
    return ''.join(random.choices(ALL_CHARS, k=code_len))


print(generate_code())              # 长度4（用默认值），例如 '59tZ'
print(generate_code(code_len=6))    # 传参覆盖默认值，例如 'FxJucw'

# 参数列表里单独出现的 * ，是个"分隔线"：它后面的参数只能用"参数名=值"来传，
# 不能靠位置传——这种参数叫"命名关键字参数"
# generate_code(6)   # ❌ TypeError：code_len是命名关键字参数，必须写成 code_len=6
# 这和Day14的*args不一样：*args是"收集"多余的位置参数；这里的*单独出现，不收集
# 任何东西，只是强制它后面的参数必须写名字，防止调用时把参数顺序传错

# random.choices() vs Day09用过的random.sample()：
# sample()不放回抽样，抽出的元素不会重复（双色球选号必须用这个，号码不能重复）
# choices()有放回抽样，可能重复选中同一个字符（验证码里字母数字重复很正常）


# ============================================================
# 二、实战：判断素数
# ============================================================
# 质数：只能被1和自身整除的大于1的正整数。Day07用穷举法判断过，这里封装成函数

def is_prime(num: int) -> bool:
    """判断num是不是质数（要求num是大于1的正整数）"""
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


print(is_prime(2))      # True
print(is_prime(97))     # True
print(is_prime(100))    # False

# num: int 和 -> bool 是"类型注解"：标注参数、返回值的类型，不影响实际运行
# （Python不会强制检查类型），但让人一眼就知道这个函数该怎么用、会返回什么
# 循环只需要试到sqrt(num)：如果到sqrt(num)都没找到因子，后面也不会有
# （比如判断100，只需要试到10，比Day07一路试到99快很多）


# ============================================================
# 三、实战：最大公约数和最小公倍数
# ============================================================
# 两个不同的功能，拆成两个函数，而不是挤到一个函数里

def gcd(x: int, y: int) -> int:
    """求最大公约数（辗转相除法）"""
    while y % x != 0:
        x, y = y % x, x
    return x


def lcm(x: int, y: int) -> int:
    """求最小公倍数"""
    return x * y // gcd(x, y)      # 函数内部调用了另一个函数


print(gcd(12, 18))    # 6
print(lcm(12, 18))    # 36

# lcm()内部直接调用了gcd()——函数之间可以互相调用
# 最小公倍数 = (x×y) ÷ 最大公约数，这是数学上的固定关系，不用重新设计算法


# ============================================================
# 四、实战：数据统计
# ============================================================
# 把常见的描述性统计指标各自封装成函数，函数之间互相调用、组合复用

def mean(data):
    """算术平均值"""
    return sum(data) / len(data)


def median(data):
    """中位数：排序后位于中间的数（偶数个取中间两个的平均）"""
    temp, size = sorted(data), len(data)
    if size % 2 != 0:
        return temp[size // 2]
    else:
        return mean(temp[size // 2 - 1:size // 2 + 1])    # 复用mean()


def ptp(data):
    """极差：最大值和最小值的差"""
    return max(data) - min(data)


def var(data, ddof=1):
    """方差（ddof=1按样本方差计算，除以n-1）"""
    x_bar = mean(data)                                      # 复用mean()
    return sum((x - x_bar) ** 2 for x in data) / (len(data) - ddof)


def std(data, ddof=1):
    """标准差：方差开平方"""
    return var(data, ddof) ** 0.5                            # 复用var()


def describe(data):
    """一次性输出所有描述性统计信息"""
    print(f'均值：{mean(data):.2f}')
    print(f'中位数：{median(data):.2f}')
    print(f'极差：{ptp(data)}')
    print(f'方差：{var(data):.2f}')
    print(f'标准差：{std(data):.2f}')


scores = [88, 92, 79, 95, 84, 91, 76]
describe(scores)

# describe()本身不做任何计算，只是把前面几个小函数"组装"调用了一遍
# 这正是函数封装的价值：小函数各自只负责一件事，组合起来就能解决复杂问题


# ============================================================
# 五、实战：给双色球选号"上色"
# ============================================================
# 复用Day14学的思路：选号和输出拆成两个函数
# 这次加一个新技巧——用ANSI转义码给终端输出上色，红球显示红色，蓝球显示蓝色

RED_BALLS = list(range(1, 34))
BLUE_BALLS = list(range(1, 17))


def choose():
    """摇一注号码，返回列表：前6个是红球，最后1个是蓝球"""
    balls = random.sample(RED_BALLS, 6)
    balls.sort()
    balls.append(random.choice(BLUE_BALLS))
    return balls


def display(balls):
    """按红/蓝上色打印一注号码"""
    for ball in balls[:-1]:                            # 切片取前6个（红球）
        print(f'\033[31m{ball:02d}\033[0m', end=' ')    # \033[31m开红色，\033[0m关闭颜色
    print(f'\033[34m{balls[-1]:02d}\033[0m')             # 最后一个（蓝球）用蓝色


n = int(input('\n生成几注双色球：'))
for _ in range(n):
    display(choose())

# \033[31m...\033[0m 是ANSI转义序列：31=红色文字，34=蓝色文字，0=重置回默认颜色
# display(choose())：先调用choose()生成一组号码，把返回值直接传给display()打印
# 调用者完全不用关心choose()内部怎么随机、display()内部怎么上色，这就是函数封装的意义
