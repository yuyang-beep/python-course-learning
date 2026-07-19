"""
Day11 - 常用数据结构之字符串
课程：Python-100-Days / Day11.常用数据结构之字符串
"""

# ============================================================
# 一、字符串也是"序列"——列表/元组学过的操作，字符串基本都支持
# ============================================================

s = 'Python'

print(s[0])          # P       索引
print(s[-1])         # n       反向索引
print(s[1:4])        # yth     切片
print(s[::-1])       # nohtyP  反转
print(s + '!!!')     # Python!!!   拼接
print(s * 2)         # PythonPython  重复
print('th' in s)     # True    成员判断
print(len(s))        # 6       长度

for ch in s:          # 遍历：逐个字符
    print(ch, end=' ')
print()


# ============================================================
# 二、字符串不可变（和元组一样）
# ============================================================

# s[0] = 'J'    # ❌ TypeError: 'str' object does not support item assignment
# 想"修改"字符串，只能生成一个新字符串，不能改原来的那个


# ============================================================
# 三、大小写相关方法
# ============================================================

msg = 'Hello, World'

print(msg.upper())             # HELLO, WORLD
print(msg.lower())              # hello, world
print(msg.swapcase())           # hELLO, wORLD   大小写互换
print('python'.capitalize())    # Python          首字母大写，其余小写
print('python 教程'.title())     # Python 教程     每个单词首字母大写（中文没有大小写，不受影响）


# ============================================================
# 四、去除首尾空白 —— 处理用户输入必备
# ============================================================

raw = '   hello python   '
print(f'[{raw.strip()}]')     # [hello python]      去掉两端空白
print(f'[{raw.lstrip()}]')    # [hello python   ]   只去左边
print(f'[{raw.rstrip()}]')    # [   hello python]   只去右边


# ============================================================
# 五、查找、替换、统计（index/count 是不是很眼熟？和列表、元组用法一样）
# ============================================================

text = 'to be or not to be'

print(text.find('be'))              # 3    第一次出现的位置；找不到返回 -1（不会报错）
print(text.find('xxx'))             # -1
print(text.index('be'))             # 3    用法同find，但找不到会报ValueError（和列表index一样）
print(text.count('be'))             # 2    出现次数
print(text.replace('be', 'BE'))       # to BE or not to BE   全部替换
print(text.replace('be', 'BE', 1))    # to BE or not to be   只替换前1个


# ============================================================
# 六、分割与连接 —— split() 和 join()，正好互为逆运算
# ============================================================

csv_line = 'Python,Java,C++,Go'
langs = csv_line.split(',')          # 按逗号切分 → ['Python', 'Java', 'C++', 'Go']
print(langs)

sentence = 'to be or not to be'
words = sentence.split()             # 不传参数：按空白切分，自动合并连续空格
print(words)

print('-'.join(langs))               # Python-Java-C++-Go   把列表拼回字符串，用 - 连接
print(' '.join(words))               # to be or not to be


# ============================================================
# 七、判断类方法（is 开头，返回 True/False，常用来校验输入合法性）
# ============================================================

print('12345'.isdigit())          # True    是否全是数字
print('abc123'.isdigit())         # False
print('python'.isalpha())         # True    是否全是字母
print('Python'.isupper())         # False   是否全部大写
print('PYTHON'.isupper())         # True
print('to be'.startswith('to'))   # True
print('to be'.endswith('be'))     # True


# ============================================================
# 八、实战：split() 和 join() 互逆 —— 解析双色球号码字符串
# 复习 Day09/10：那边用 join() 把号码拼成字符串打印出来
# 这里反过来，用 split() 把字符串还原成数字
# ============================================================

text = input('\n请输入号码，用空格分隔（如 3 7 15 22 28 33）：')

parts = text.split()                          # split()：字符串 → 列表
print('split() 结果：', parts)

nums = [int(p) for p in parts if p.isdigit()]  # isdigit()先过滤掉非数字项，再转成int
print(f'共{len(nums)}个有效号码，总和{sum(nums)}，最大{max(nums)}，最小{min(nums)}')

rebuilt = ' '.join(parts)                      # join()：列表 → 字符串，是split的逆运算
print('join() 结果：', rebuilt)
print('和原始输入（去空白后）相同：', rebuilt == text.strip())
