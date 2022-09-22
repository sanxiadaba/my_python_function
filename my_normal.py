# 日常使用的函数
import time
from datetime import datetime

import snoop
from icecream import ic

# 是否打印分割线的宏
print_line = True
snoop = snoop


# 打印的时间前缀 见https://blog.csdn.net/shomy_liu/article/details/44141483
def time_format():
    # 时间前缀，时分秒微秒
    return f"{datetime.now().strftime('%H:%M:%S %f')}|> "


# 这里将输出前缀绑定到指定函数上，并且打印行数、文件名
ic.configureOutput(prefix=time_format, includeContext=True)
debug = ic


# 打印分割线的函数
def line(n: int):
    if print_line:
        print("\033[1;31;40m", (" " + str(n) + " ").center(80, "="), "\033[0m")
    else:
        pass


# 关闭打印变量和行数
def close_debug_line():
    # 上升为全局变量
    global print_line
    print_line = False
    debug.disable()


# 计算函数运行时间,默认运行时间保留三位小数
def function_time(func, *args, **kwargs):
    begin = time.time()
    f = func(*args, **kwargs)
    end = time.time()
    s = '{}()：{:.%sf} s' % 3
    print(s.format(func.__name__, end - begin))
    return f
