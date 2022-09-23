# 测试每个功能的使用
import time
from collections import OrderedDict

import my_info
import my_normal

# 这行的注释解开后不会进行变量的打印和分割线的打印
# my_normal.close_debug_line()

# 一些用来测试的变量、函数
my_str = "hello"
n = 100


# 睡眠指定时间
def sleep_time(n):
    time.sleep(n + 1.1)


# 测试分割线
def test_line():
    my_normal.line(100)
    my_normal.line(1)


# 打印信息
def test_info():
    my_info.get_all_info()


# 打印变量
def test_var():
    my_normal.debug(my_str)
    my_normal.debug(n)


# 测试打印函数的时间
def test_time():
    my_normal.function_time(sleep_time, 1)


# 使用snoop进行调试
def test_snoop():
    # 先是最简单的使用,直接在一个函数上面添加装饰器进行调试
    # 注意：默认只能看一层函数的一般变量
    @my_normal.snoop
    def number_to_bits(number):
        if number:
            bits = []
            while number:
                number, remainder = divmod(number, 2)
                bits.insert(0, remainder)
            return bits
        else:
            return [0]

    number_to_bits(6)
    my_normal.line(1)

    # 查看两层函数
    @my_normal.snoop
    def maa():
        a = 1
        b = 2

        def mab():
            c = 100
            print(a + b + c)

        print(a + b)

    maa()
    my_normal.line(2)

    # 调试一段代码
    with my_normal.snoop:
        sum = 0
        for i in range(10):
            sum += i
        my_normal.debug(sum)
    my_normal.line(2)

    # 展开变量，对复杂类型进行穿透
    class Foo(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

    @my_normal.snoop.snoop(watch_explode=('_d', '_point', 'lst + []'))
    def maa():
        _d = OrderedDict([('a', 1), ('b', 2), ('c', 'ignore')])
        _point = Foo(x=3, y=4)
        lst = [7, 8, 9, 10]

    maa()
