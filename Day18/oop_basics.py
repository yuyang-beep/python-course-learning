"""
Day18 - 面向对象编程入门
课程：Python-100-Days / Day18.面向对象编程入门
"""
# 面向对象编程（OOP）是一种编程范式：把数据和处理数据的方法绑成一个整体，
# 这个整体叫"对象"；把行为相同的对象抽取共同特征，就得到了"类"。
# 类是抽象的模板，对象是类的具体实例。三大支柱：封装、继承、多态——本节先讲封装，
# 继承和多态留到后面的课程


# ============================================================
# 一、定义类、创建对象——类是模板，对象是实例
# ============================================================

# 1.1 用class关键字定义类：类体里的函数叫"方法"，第一个参数习惯写self，
# 代表"接收这条消息的对象自己"（谁调用这个方法，self就是谁）
class Student:

    def study(self, course_name):
        print(f'学生正在学习{course_name}.')

    def play(self):
        print('学生正在玩游戏.')


# 1.2 构造器语法：类名加圆括号，创建这个类的对象
stu1 = Student()
stu2 = Student()
print(stu1)    # <__main__.Student object at 0x...>——打印的是对象在内存中的地址
print(stu2)    # 地址和stu1不同——是另一个独立对象
print(hex(id(stu1)), hex(id(stu2)))    # 和上面print(stu1)显示的地址一致

# stu1、stu2变量里存的不是对象本身，而是对象的内存地址（类似指路的门牌号）。
# 所以下面这行不会创建新对象，只是让stu3和stu2指向同一个门牌号：
stu3 = stu2
print(stu3 is stu2)    # True——同一个对象，两个变量名而已


# 1.3 给对象发消息=调用对象的方法，Python提供两种等价写法
# 写法一："类.方法(对象, 其余参数)"——对象作为第一个参数，手动传给self
Student.study(stu1, 'Python程序设计')    # 学生正在学习Python程序设计.
# 写法二："对象.方法(其余参数)"——更常用，点前面的对象自动传给self，不用手动写
stu1.study('Python程序设计')             # 学生正在学习Python程序设计.

Student.play(stu2)     # 学生正在玩游戏.
stu2.play()             # 学生正在玩游戏.
# 两种写法效果完全一样，写法二只是Python帮你把"点前面的对象"自动填进了self——
# 语法糖，和Day17@装饰器语法糖是同一个思路：省略重复书写


# ============================================================
# 二、__init__初始化方法——给对象一出生就带上属性
# ============================================================

# 2.1 目前的Student对象只有行为（study/play），没有属性（姓名、年龄）。
# __init__是Python留给"对象初始化"的专用方法名（Day17讲过的"Python自己的地盘"）：
# 调用Student()构造对象时，Python会自动执行__init__，把传入的参数存成对象的属性
class Student:
    """学生"""

    def __init__(self, name, age):
        """初始化方法：创建对象时自动调用，负责给对象装上初始属性"""
        self.name = name    # self.xxx = ... 就是"给这个对象装上一个叫xxx的属性"
        self.age = age

    def study(self, course_name):
        """学习"""
        print(f'{self.name}正在学习{course_name}.')

    def play(self):
        """玩耍"""
        print(f'{self.name}正在玩游戏.')


# 2.2 构造对象时把name、age当参数传进去，Student()背后其实是Python调用了__init__
stu1 = Student('骆昊', 44)
stu2 = Student('王大锤', 25)
stu1.study('Python程序设计')    # 骆昊正在学习Python程序设计.
stu2.play()                     # 王大锤正在玩游戏.
print(stu1.name, stu1.age)      # 骆昊 44——属性可以直接用"对象.属性名"读取

# 2.3 两个对象的属性值互不相同（这里name、age就不同），
# 说明每次创建对象都会独立执行一次__init__、分配一份自己的属性空间，
# 不会因为都是Student类就共享同一份数据——这正是"类是模板、对象是独立实例"的体现
print(stu1.name == stu2.name, stu1 is stu2)    # False False——姓名不同，也不是同一个对象


# ============================================================
# 三、封装——只暴露"怎么用"，藏起"怎么实现"
# ============================================================

# 3.1 封装：把方法内部具体怎么做的细节藏起来，外部只需要知道方法名和该传什么参数，
# 不需要关心内部是怎么实现的。类比：坐电梯只需要按楼层按钮（外部接口），
# 不需要知道电机、钢缆、变频器是怎么配合运转的（内部实现细节）
class Robot:
    """机器人"""

    def __init__(self, name):
        self.name = name

    def pour_water(self):
        """倒水——内部一大串具体动作，调用者完全不用知道"""
        print(f'{self.name}：站起→走到桌边→拿起水杯→接水→端回来，水倒好了')


robot = Robot('小艾')
robot.pour_water()    # 小艾：站起→走到桌边→拿起水杯→接水→端回来，水倒好了
# 调用者只发了一条"倒水"的消息，不用像操作机械那样一条条下达"向左转、走5步..."的指令，
# 这就是封装带来的好处：复杂度被"折叠"进了方法内部


# 3.2 面向对象编程的常规套路是"三步走"：①定义类 → ②创建对象 → ③给对象发消息。
# 但如果需要的类已经存在，第①步可以省略——比如内置的list、set、dict其实也是类：
print(type([1, 2, 3]))     # <class 'list'>——方括号语法背后也是在创建一个list类的对象
print(type({1, 2, 3}))     # <class 'set'>
print(type({'a': 1}))      # <class 'dict'>
# 这也是为什么list有.append()、dict有.get()这些"方法"——它们和study()、play()
# 本质上是一回事，只是这些类是Python内置的，不需要我们自己写class语句


# ============================================================
# 四、案例实战
# ============================================================

# 4.1 数字时钟：属性是时/分/秒，run()让时间走一格，show()把时间格式化成字符串
import time


class Clock:
    """数字时钟"""

    def __init__(self, hour=0, minute=0, second=0):
        """初始化方法
        :param hour: 时
        :param minute: 分
        :param second: 秒
        """
        self.hour = hour
        self.min = minute
        self.sec = second

    def run(self):
        """走字：秒满60进分，分满60进时，时满24归零"""
        self.sec += 1
        if self.sec == 60:
            self.sec = 0
            self.min += 1
            if self.min == 60:
                self.min = 0
                self.hour += 1
                if self.hour == 24:
                    self.hour = 0

    def show(self):
        """显示时间，格式化成HH:MM:SS，个位数补0"""
        return f'{self.hour:0>2d}:{self.min:0>2d}:{self.sec:0>2d}'


# 课程原文里是while True死循环，让时钟一直走、每秒打印一次，适合单独运行的脚本；
# 这里改成走6步、不真的sleep，方便一次性看到完整的进位过程
clock = Clock(23, 59, 58)
for _ in range(6):
    print(clock.show())    # 23:59:58 → 23:59:59 → 00:00:00 → 00:00:01 → 00:00:02 → 00:00:03
    clock.run()


# 4.2 平面上的点：__str__是另一个"Python自己的地盘"的魔法方法——
# 定义了它之后，print(对象)不再显示"<__main__.Point object at 0x...>"这种地址，
# 而是显示__str__返回的字符串，因为print内部就是通过调用__str__来决定"打印成什么样"
class Point:
    """平面上的点"""

    def __init__(self, x=0, y=0):
        """初始化方法
        :param x: 横坐标
        :param y: 纵坐标
        """
        self.x, self.y = x, y

    def distance_to(self, other):
        """计算与另一个点的距离（勾股定理）
        :param other: 另一个点
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5

    def __str__(self):
        return f'({self.x}, {self.y})'


p1 = Point(3, 5)
p2 = Point(6, 9)
print(p1)                  # (3, 5)——调用了__str__，不是默认的地址格式
print(p2)                  # (6, 9)
print(p1.distance_to(p2))  # 5.0——dx=3, dy=4，勾股定理√(3²+4²)=5


# 对比：如果Point没有定义__str__，print(p1)会打印成什么样？
class PointNoStr:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y


p3 = PointNoStr(3, 5)
print(p3)    # <__main__.PointNoStr object at 0x...>——没有__str__，退回Python默认的"地址"表示法
