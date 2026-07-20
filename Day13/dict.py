"""
Day13 - 常用数据结构之字典
课程：Python-100-Days / Day13.常用数据结构之字典
"""

# ============================================================
# 一、为什么需要字典？
# ============================================================
# 列表/元组靠"位置"存取元素，但很多数据用"名字"取更自然
# 比如想存"每个人的分数"，用列表得先查位置，很绕：

names  = ['小明', '小红', '小刚']
scores = [90, 85, 78]
print(scores[names.index('小红')])    # 85 —— 得先在names里查位置，再去scores里取

# 字典（dict）直接用"键(key)"对应"值(value)"，取值不用记位置：
scores_dict = {'小明': 90, '小红': 85, '小刚': 78}
print(scores_dict['小红'])            # 85 —— 直接按名字取


# ============================================================
# 二、创建字典
# ============================================================

d1 = {'a': 1, 'b': 2}              # 直接用 {} 写键值对
d2 = dict(a=1, b=2)                 # 用 dict() 加关键字参数创建（键不用加引号）
d3 = dict([('a', 1), ('b', 2)])     # 用 dict() 把"键值对的列表"转成字典
d4 = {}                              # 空字典——这次 {} 就是字典本身（Day12讲过空集合不能用{}，要用set()）

print(d1)          # {'a': 1, 'b': 2}
print(d2)          # {'a': 1, 'b': 2}
print(d3)          # {'a': 1, 'b': 2}
print(type(d4))    # <class 'dict'>


# ============================================================
# 三、存取元素
# ============================================================

student = {'name': 'Tom', 'age': 18}

print(student['name'])            # Tom     —— 用 [键] 取值
# print(student['score'])         # ❌ KeyError: 'score'  ——键不存在会报错

print(student.get('score'))          # None   —— get()更安全，键不存在返回None，不报错
print(student.get('score', 0))       # 0      —— 还可以指定"找不到时的默认值"


# ============================================================
# 四、增加和修改——用的是同一句语法
# ============================================================

student['score'] = 95      # 'score'原本不存在 → 新增一个键值对
print(student)              # {'name': 'Tom', 'age': 18, 'score': 95}

student['age'] = 19         # 'age'已经存在 → 修改它的值，位置不变
print(student)              # {'name': 'Tom', 'age': 19, 'score': 95}


# ============================================================
# 五、删除元素
# ============================================================

student['temp'] = 'x'
del student['temp']              # 删除指定键，键不存在会报KeyError
removed = student.pop('score')   # 删除并返回被删掉的值
print(removed)                    # 95
print(student)                    # {'name': 'Tom', 'age': 19}


# ============================================================
# 六、遍历字典 —— keys() / values() / items()
# ============================================================

scores_dict = {'小明': 90, '小红': 85, '小刚': 78}

for name in scores_dict:                  # 直接遍历字典，拿到的是键（默认行为，等价于遍历keys()）
    print(name, end=' ')
print()

for score in scores_dict.values():        # 遍历所有值
    print(score, end=' ')
print()

for name, score in scores_dict.items():   # 遍历"键值对"，直接拆包成两个变量，最常用
    print(f'{name}:{score}', end='  ')
print()


# ============================================================
# 七、成员判断 —— in 判断的是"键"，不是值
# ============================================================

print('小明' in scores_dict)       # True   —— 判断键是否存在
print(90 in scores_dict)            # False  —— 90是值不是键，所以不在
print(90 in scores_dict.values())   # True   —— 想判断值在不在，要去values()里找


# ============================================================
# 八、字典推导式
# ============================================================

nums = [1, 2, 3, 4, 5]
squares = {n: n ** 2 for n in nums}     # 键是数字本身，值是它的平方
print(squares)   # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}


# ============================================================
# 九、实战：统计双色球红球出现频率
# 生成n注号码，用字典当"计数器"——键是球号，值是出现次数
# ============================================================

import random

n = int(input('\n生成几注双色球，统计红球出现频率：'))
red_balls = list(range(1, 34))

counter = {}                       # 空字典：key=红球号码，value=出现次数
for _ in range(n):
    selected = random.sample(red_balls, 6)
    for ball in selected:
        counter[ball] = counter.get(ball, 0) + 1   # 见过就+1，没见过get()给默认值0

# 字典从Python 3.7起会保留插入顺序（这点和Day12的集合不一样），这里按球号首次出现的顺序打印
for ball, times in counter.items():
    print(f'{ball:02d}号：出现{times}次')

# 找出现次数最多的号码——还没学函数/lambda，先用最朴素的循环比较
most_ball, most_times = None, 0
for ball, times in counter.items():
    if times > most_times:
        most_ball, most_times = ball, times
print(f'\n出现最多的是{most_ball:02d}号，共{most_times}次')
