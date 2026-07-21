"""
Day16 - 函数使用进阶
课程：Python-100-Days / Day16.函数使用进阶
"""
# Python中的函数是"一等公民"（一等函数）：函数可以赋值给变量、可以作为参数传给别的函数、
# 也可以作为函数的返回值。把函数当参数或返回值使用的函数，叫"高阶函数"


# ============================================================
# 一、高阶函数——把函数本身当参数传递
# ============================================================

# 1.1 回顾Day14的calc()：只能做加法，"+="把运算方式写死在函数内部
def calc_old(*args, **kwargs):
    items = list(args) + list(kwargs.values())
    result = 0
    for item in items:
        if type(item) in (int, float):
            result += item
    return result


print(calc_old(1, 2, 3, 4, 5))    # 15，但只能求和，改不了运算规则

# 1.2 把"怎么运算"也变成参数——传入不同的二元运算函数，同一个calc就能做加法/乘法/...
def add(x, y):
    return x + y


def mul(x, y):
    return x * y


def calc(init_value, op_func, *args, **kwargs):
    """init_value：运算初始值；op_func：做运算的函数；其余参数是参与运算的数据"""
    items = list(args) + list(kwargs.values())
    result = init_value
    for item in items:
        if type(item) in (int, float):
            result = op_func(result, item)     # 调用传进来的函数，而不是写死的运算符
    return result


print(calc(0, add, 1, 2, 3, 4, 5))    # 15  —— 求和：初始值0 + 加法函数
print(calc(1, mul, 1, 2, 3, 4, 5))    # 120 —— 求积：初始值1 + 乘法函数，同一个calc()做到两种运算

# 注意：这里传的是add、mul（函数名，不带括号）——不带括号的函数名代表函数本身这个对象，
# 可以像普通数据一样传来传去；一旦加上括号add()，就变成"调用"，会立刻执行并拿到结果

# 标准库operator模块提供了现成的运算函数，不用自己定义add/mul
import operator

print(calc(0, operator.add, 1, 2, 3, 4, 5))   # 15
print(calc(1, operator.mul, 1, 2, 3, 4, 5))   # 120


# ============================================================
# 二、内置高阶函数：filter / map / sorted
# ============================================================

def is_even(num):
    """判断num是不是偶数"""
    return num % 2 == 0


def square(num):
    """求平方"""
    return num ** 2


old_nums = [35, 12, 8, 99, 60, 52]

# filter(函数, 序列)：只保留让函数返回True的元素——这里筛出偶数
# map(函数, 序列)：对序列每个元素做同样的加工——这里对每个数求平方
# filter/map返回的都不是列表本身（是惰性的迭代器），要用list()才能看到内容
new_nums = list(map(square, filter(is_even, old_nums)))
print(new_nums)     # [144, 64, 3600, 2704] —— 先filter筛出偶数[12,8,60,52]，再map逐个平方

# 等价写法：Day09学过的列表生成式，一行搞定筛选+加工，更简洁
new_nums2 = [num ** 2 for num in old_nums if num % 2 == 0]
print(new_nums2)     # [144, 64, 3600, 2704]，结果和filter+map完全一样

# sorted(序列, key=函数)：按自定义规则排序；不会修改原列表，而是返回一个排好序的新列表
# （这叫"无副作用"：调用函数除了给出返回值，不改变外部任何状态——和list.sort()直接改原列表不同）
old_strings = ['in', 'apple', 'zoo', 'waxberry', 'pear']
print(sorted(old_strings))            # ['apple', 'in', 'pear', 'waxberry', 'zoo']  —— 默认按字母顺序
print(sorted(old_strings, key=len))   # ['in', 'zoo', 'pear', 'apple', 'waxberry']  —— key=len，按长度排序


# ============================================================
# 三、lambda——匿名函数
# ============================================================
# 如果传给高阶函数的逻辑只有一行、也不需要起名字复用，可以用lambda就地定义
# 语法：lambda 参数: 表达式   —— 不写def，不写return，表达式的运算结果就是返回值

new_nums3 = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, old_nums)))
print(new_nums3)     # [144, 64, 3600, 2704] —— 效果和上面is_even+square完全一样，省去单独定义两个函数

# 函数是"一等公民"：lambda也可以先赋值给变量，当成普通函数一样调用
import functools

fac = lambda n: functools.reduce(operator.mul, range(2, n + 1), 1)
print(fac(6))         # 720，即6! —— reduce把range(2,7)=[2,3,4,5,6]依次用mul累乘，初始值1

is_prime = lambda x: all(map(lambda f: x % f, range(2, int(x ** 0.5) + 1)))
print(is_prime(37))   # True

# reduce(函数, 序列, 初始值)：归约操作——把序列元素从初始值开始，依次两两运算成一个值，
# 思路和上面的calc()一样，只是reduce是标准库现成的，不用自己写循环
# is_prime这行：对range(2,√x+1)里每个因子f算x%f，如果都不是0（都为真值），all()才返回True
# all(序列)：序列里所有元素都为真（非0/非空）才返回True，只要有一个假值就返回False


# ============================================================
# 四、偏函数——固定住部分参数，生成一个新函数
# ============================================================
# functools.partial(函数, 固定参数=值)：返回一个新函数，调用新函数时不用再传已固定的参数

int2 = functools.partial(int, base=2)      # 固定base=2，新函数int2只需要传字符串
int8 = functools.partial(int, base=8)
int16 = functools.partial(int, base=16)

print(int('1001'))     # 1001 —— 不传base，int()默认按十进制解析
print(int2('1001'))    # 9    —— 按二进制解析：1001(2) = 1*8+0*4+0*2+1*1 = 9
print(int8('1001'))    # 513  —— 按八进制解析：1001(8) = 1*512+0+0+1 = 513
print(int16('1001'))   # 4097 —— 按十六进制解析：1001(16) = 1*4096+0+0+1 = 4097

# 不用偏函数的话，每次转换都要写int('1001', base=2)，重复传相同的base参数；
# 偏函数把"不会变"的参数提前锁死在新函数里，之后调用更省事，也不容易漏传/传错
