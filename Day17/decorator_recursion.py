"""
Day17 - 函数高级应用
课程：Python-100-Days / Day17.函数高级应用
"""
# 本节两个重点：装饰器（不修改原函数代码，给函数"追加"能力）
# 和递归调用（函数直接或间接调用自身）


# ============================================================
# 一、装饰器——不修改原函数代码，给函数"加"能力
# ============================================================

import random
import time


def download(filename):
    """下载文件（用随机短暂休眠模拟耗时，不是真的联网下载）"""
    print(f'开始下载{filename}')
    time.sleep(random.random())
    print(f'{filename}下载完成')


def upload(filename):
    """上传文件"""
    print(f'开始上传{filename}')
    time.sleep(random.random())
    print(f'{filename}上传完成')


download('data.zip')
upload('report.pdf')

# 1.1 需求：想知道download函数到底花了多少时间——最直接的办法是调用前后各记一次时间
start = time.time()
download('data.zip')
end = time.time()
print(f'耗时：{end - start:.2f}秒')

# 如果upload也要计时，得把"记开始时间→调用→记结束时间→算差值→打印"这5行代码原样再抄一遍
# ——典型的重复代码。但这次没法像Day14那样简单封装成一个函数：要包住的是"调用某个函数"
# 这个动作本身，而且以后可能还有别的函数也要计时，函数种类不确定。这正是装饰器要解决的问题


# 1.2 装饰器的结构：一个函数，参数是"被装饰的函数"，返回值是"包了一层新能力的函数"
def record_time(func):
    def wrapper(*args, **kwargs):               # *args/**kwargs照单全收，不管func要什么参数
        start = time.time()
        result = func(*args, **kwargs)           # 真正执行被装饰的函数，参数原样转发
        end = time.time()
        print(f'{func.__name__}执行时间：{end - start:.2f}秒')
        return result                             # 别忘了把func的返回值原样传回去
    return wrapper


# 1.3 用法一：手动调用装饰器，用返回值替换原函数
download = record_time(download)
download('data.zip')      # 现在调用的其实是wrapper，多了自动计时的能力


# 1.4 用法二：@装饰器名——语法糖，效果和"手动替换"完全一样，只是写法更简洁
@record_time
def upload(filename):
    print(f'开始上传{filename}')
    time.sleep(random.random())
    print(f'{filename}上传完成')


upload('report.pdf')      # upload定义时就已经被record_time包了一层
# @record_time
# def upload(filename): ...
# 等价于：
# def upload(filename): ...
# upload = record_time(upload)
# @写法只是把"定义函数"和"装饰函数"合并成了一步，不用重复写函数名


# 1.5 functools.wraps——保留被装饰前的原函数，方便必要时"绕过"装饰器
from functools import wraps


def record_time2(func):
    @wraps(func)                                 # 把func的__name__等信息"复制"给wrapper，并挂一个__wrapped__指回func
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__}执行时间：{end - start:.2f}秒')
        return result
    return wrapper


@record_time2
def greet(name):
    """打招呼"""
    return f'你好，{name}'


print(greet('小明'))                 # 走装饰后的wrapper，会先打印一行执行时间，再打印问候语
print(greet.__wrapped__('小红'))     # 通过__wrapped__拿到原始greet，绕开装饰器，不计时

# 装饰器函数本身也是可以参数化的（比如下面lru_cache()带的括号），下面递归部分会用到


# ============================================================
# 二、递归调用——函数直接或间接调用自身
# ============================================================

# 2.1 递归版阶乘：数学定义N! = N × (N-1)!，定义本身就是"递归"的
def fac(num):
    if num in (0, 1):             # 收敛条件：算到0或1就不再往下调用，直接返回1
        return 1
    return num * fac(num - 1)      # 递归公式：调用自己，规模减1


print(fac(5))     # 120
# 展开看fac(5)怎么算的：
# 5*fac(4) = 5*(4*fac(3)) = 5*(4*(3*fac(2))) = 5*(4*(3*(2*fac(1))))
# fac(1)命中收敛条件直接返回1，再从里往外一层层乘回去：2*1=2，3*2=6，4*6=24，5*24=120

# 每次调用fac()，内存里的"栈"（stack，先进后出的结构）就多一层"栈帧"记录当前进度，
# 函数返回则减一层栈帧；如果递归层数太多（栈帧摞太高），栈会被撑爆，
# 抛出RecursionError（栈溢出）。CPython默认最多允许约1000层，试试fac(5000)：
try:
    fac(5000)
except RecursionError as e:
    print('递归层数太深，栈溢出：', e)


# 2.2 递归版斐波那契：f(n) = f(n-1) + f(n-2)，同样是天然的递归定义
def fib_recursive(n):
    if n in (1, 2):
        return 1
    return fib_recursive(n - 1) + fib_recursive(n - 2)


print(fib_recursive(10))     # 55

# 2.3 但递归版斐波那契有严重的性能问题：算fib(n)会重复算很多次fib(n-2)、fib(n-3)……
# 改用循环递推（Day07学过的a, b = b, a+b同步赋值技巧），效率高得多
def fib_loop(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


print(fib_loop(10))          # 55，结果和递归版一样，但不会有大量重复计算


# 2.4 用装饰器实测对比两种写法的性能差距——不用改fib_recursive/fib_loop一个字，
# 只在外面包一层record_time，这正是装饰器"复用、不侵入原代码"的价值
@record_time
def test_recursive():
    return fib_recursive(28)


@record_time
def test_loop():
    return fib_loop(28)


print(test_recursive())
print(test_loop())
# 能明显看到递归版慢得多——n每增加1，递归调用次数接近翻倍，是指数级增长


# 2.5 用functools.lru_cache给递归版"加缓存"，不用重写成循环也能大幅提速
from functools import lru_cache


@lru_cache()
def fib_cached(n):
    if n in (1, 2):
        return 1
    return fib_cached(n - 1) + fib_cached(n - 2)


@record_time
def test_cached():
    return fib_cached(28)


print(test_cached())
# lru_cache把每个n对应的结果缓存起来，递归过程中重复调用fib_cached(同一个n)时直接查表返回，
# 不会重新展开计算——不改fib_cached内部一行逻辑，只加一行@lru_cache()就解决了重复计算问题，
# 这也是"装饰器能优雅扩展函数能力"的一个典型例子
