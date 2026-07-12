"""
Day05 - 分支结构
课程：Python-100-Days / Day05.分支结构
"""

# ============================================================
# 一、if / else 基本结构
# ============================================================
# 语法：
#   if 条件:
#       条件为 True 时执行（注意缩进4个空格）
#   else:
#       条件为 False 时执行

score = int(input('输入你的分数：'))
if score >= 60:
    print('及格了！')
else:
    print('不及格，继续加油！')


# ============================================================
# 二、if / elif / else 多分支
# ============================================================

score2 = float(input('再输入一个百分制成绩：'))
if score2 >= 90:
    grade = 'A'
elif score2 >= 80:
    grade = 'B'
elif score2 >= 70:
    grade = 'C'
elif score2 >= 60:
    grade = 'D'
else:
    grade = 'E'
print(f'等级：{grade}')


# ============================================================
# 三、实战：BMI 计算器（综合 input / 运算符 / 分支）
# ============================================================

height = float(input('身高（cm）：'))
weight = float(input('体重（kg）：'))
bmi = weight / (height / 100) ** 2
print(f'你的 BMI = {bmi:.1f}')

if bmi < 18.5:
    print('体重偏轻')
elif bmi < 24:
    print('身材正常，继续保持！')
elif bmi < 27:
    print('体重偏重')
elif bmi < 30:
    print('轻度肥胖')
elif bmi < 35:
    print('中度肥胖')
else:
    print('重度肥胖')


# ============================================================
# 【练习】：判断三条边能否构成三角形，能的话输出面积
# 条件：任意两边之和 > 第三边
# 面积公式（海伦公式）：area = sqrt(s*(s-a)*(s-b)*(s-c))，s = (a+b+c)/2
# ============================================================

a = float(input('输入边长 a：'))
b = float(input('输入边长 b：'))
c = float(input('输入边长 c：'))

if a + b > c and a + c > b and b + c > a:
    perimeter = a + b + c
    s = perimeter / 2
    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
    print(f'周长：{perimeter:.2f}，面积：{area:.2f}')
else:
    print('这三条边不能构成三角形')
