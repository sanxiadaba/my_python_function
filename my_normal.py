# 日常使用的函数
import inspect
import re


# 打印分割线的函数
def line(n: int):
    print("\033[1;31;40m", (" " + str(n) + " ").center(80, "="), "\033[0m")


# 打印变量名的函数
def varname(var):
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
        if m:
            print(m.group(1))
