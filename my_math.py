# 关于数学的一些函数
# 进行了加速处理
import random
import time
from functools import lru_cache
from typing import List

import taichi as ti

ti.init(arch=ti.gpu,
        random_seed=int(time.time()),
        default_fp=ti.f32,
        default_ip=ti.i32)


# 对prop_true进行并行处理
@ti.kernel
def process_prop_true(res: ti.template(), f: ti.f32):
    for i in res:
        if ti.random(dtype=float) < f:
            res[i] = 1
        else:
            res[i] = 0


# 输入一个大于0小于1的小数，这个函数有这个小数的概率输出True 否则是 False
# 第二个参数表示的是进行几次判断，返回的是一个列表
def prop_true(n: int, f: float) -> ti.template():
    res = ti.field(dtype=ti.i32, shape=n)
    process_prop_true(res, f)
    # return [bool(i) for i in list(res.to_numpy())]
    return res


# 不使用taichi的情况
def test_random(n: int, f: float):
    res = []
    for i in range(n):
        if random.random() < f:
            res.append(1)
        else:
            res.append(0)
    return res


m = 1
n = 100_0000
f = 0.1

t1 = time.time()
for _ in range(m):
    prop_true(n, f)
print(time.time() - t1)
# print(prop_true(m, f))

t1 = time.time()
for _ in range(m):
    test_random(n, f)
print(time.time() - t1)
