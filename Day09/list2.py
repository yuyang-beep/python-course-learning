"""
Day09 - 常用数据结构之列表（下）
课程：Python-100-Days / Day09.常用数据结构之列表-2
"""

# ============================================================
# 一、列表的常用方法
# ============================================================

langs = ['Python', 'Java', 'C++']

# 添加元素
langs.append('Go')           # 追加到末尾
langs.insert(1, 'SQL')       # 插入到索引1的位置
print(langs)                 # ['Python', 'SQL', 'Java', 'C++', 'Go']

# 删除元素
langs.remove('Java')         # 删除第一个匹配的元素
langs.pop()                  # 删除并返回最后一个元素
item = langs.pop(1)          # 删除并返回索引1的元素
print(item)                  # SQL
print(langs)                 # ['Python', 'C++']

# 查找元素
items = ['Python', 'Java', 'Java', 'C++', 'Python']
print(items.index('Python'))      # 第一次出现的位置 → 0
print(items.index('Python', 1))   # 从索引1开始找 → 4
print(items.count('Java'))        # 出现次数 → 2

# 排序和反转
nums = [5, 2, 8, 1, 9, 3]
nums.sort()             # 从小到大排序（直接修改原列表）
print(nums)             # [1, 2, 3, 5, 8, 9]
nums.sort(reverse=True) # 从大到小
print(nums)             # [9, 8, 5, 3, 2, 1]
nums.reverse()          # 反转顺序
print(nums)             # [1, 2, 3, 5, 8, 9]

# 清空列表
temp = [1, 2, 3]
temp.clear()
print(temp)             # []


# ============================================================
# 二、列表生成式（重要！用一行代替多行循环）
# ============================================================
# 语法：[表达式 for 变量 in 序列 if 条件]

# 普通写法
items = []
for i in range(1, 11):
    items.append(i ** 2)
print(items)   # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# 生成式写法（推荐）
items = [i ** 2 for i in range(1, 11)]
print(items)   # 结果完全相同

# 带条件的生成式：取1~99中能被3或5整除的数
items = [i for i in range(1, 100) if i % 3 == 0 or i % 5 == 0]
print(items)

# 对现有列表加工
nums = [35, 12, 97, 64, 55]
doubled = [n * 2 for n in nums]       # 每个元素乘2
big = [n for n in nums if n > 50]     # 只保留大于50的
print(doubled)   # [70, 24, 194, 128, 110]
print(big)       # [97, 64, 55]


# ============================================================
# 三、嵌套列表（列表里的列表）
# ============================================================

# 用嵌套列表表示5个学生3门课的成绩
import random
scores = [[random.randrange(60, 101) for _ in range(3)] for _ in range(5)]
print(scores)
print(scores[0])      # 第1个学生的3门成绩
print(scores[0][1])   # 第1个学生的第2门成绩


# ============================================================
# 四、实战：双色球随机选号
# 红球：从1~33中选6个（不重复）
# 蓝球：从1~16中选1个
# ============================================================

n = int(input('\n生成几注双色球号码：'))
red_balls  = list(range(1, 34))   # 1~33
blue_balls = list(range(1, 17))   # 1~16

for i in range(n):
    selected = random.sample(red_balls, 6)  # 无放回抽6个
    selected.sort()
    blue = random.choice(blue_balls)
    red_str  = ' '.join([f'{b:02d}' for b in selected])
    print(f'第{i+1}注：红球 [{red_str}]  蓝球 [{blue:02d}]')
