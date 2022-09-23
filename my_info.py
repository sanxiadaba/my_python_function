import platform
from datetime import datetime

import pkg_resources
import psutil
import pynvml


# B转换为通用的内存大小
# 这里传的单位的Bytes 后缀是B
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


# 获取启动时间
def get_boot_time():
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    print(f"当前系统启动时间: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")


# 获取系统信息
def get_system_info():
    print("=" * 40 + "系统信息" + "=" * 40)
    get_boot_time()
    uname = platform.uname()
    print(f"计算机名称: {uname.node}")
    print(f"系统: {uname.system}")
    print(f"系统版本: {uname.release}")
    print(f"版本号: {uname.version}")
    print(f"系统类型: {uname.machine}")
    print()


# 获取cpu的信息
def get_cpu_info():
    print("=" * 40 + "CPU 信息" + "=" * 40 + "")
    uname = platform.uname()
    print(f"处理器型号: {uname.processor}")
    print(f"物理核心数:{psutil.cpu_count(logical=False)}")
    print(f"实际核心数:{psutil.cpu_count(logical=True)}")
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    print(f"最高主频: {cpufreq.max:.2f}Mhz")
    print(f"最低主频: {cpufreq.min:.2f}Mhz")
    print(f"当前频率: {cpufreq.current:.2f}Mhz")
    # CPU usage
    print("核心使用详细:\n")
    for i, percentage in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
        print(f"    Core {i}: {percentage}%")
    print(f"总体使用率: {psutil.cpu_percent()}%")
    print()


# 获取内存信息
def get_memory_info():
    # Memory Information
    print("=" * 40 + "内存信息" + "=" * 40)
    # get the memory details
    svmem = psutil.virtual_memory()
    print(f"内存总大小: {get_size(svmem.total)}")
    print(f"可用内存大小: {get_size(svmem.available)}")
    print(f"已使用内存大小: {get_size(svmem.used)}")
    print(f"内存使用率: {svmem.percent}%")
    print()


# 获取硬盘信息
def get_disk_info():
    # DISK Information
    print("=" * 40 + "硬盘信息" + "=" * 40)
    partitions = psutil.disk_partitions()
    total_disk = 0
    for partition in partitions:
        print(f"{partition.device}盘： ")
        print(f"    文件格式: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        total_disk += partition_usage.total
        print(f"    总大小: {get_size(partition_usage.total)}")
        print(f"    已使用: {get_size(partition_usage.used)}")
        print(f"    还剩余: {get_size(partition_usage.free)}")
        print(f"    使用率: {partition_usage.percent}%")
        print()
    print(f"硬盘总大小: {get_size(total_disk)},总共分区数：{len(partitions)}")
    print()


# 获取python的版本信息
def get_python_info():
    print("=" * 40 + "Python信息" + "=" * 40)
    print("Python解释器版本： ", platform.python_branch())
    print("构建器信息： ", platform.python_build())
    print("编译器信息： ", platform.python_compiler())
    print("解释器发行版本： ", platform.python_implementation())
    # 以元组的形式返回版本信息 ('3', '7', '0')
    print("具体版本", platform.python_version_tuple())
    print()


# 获取pip已安装的包
def get_pip_info():
    print("=" * 40 + "pip已安装包" + "=" * 40)
    dists = [d for d in pkg_resources.working_set]
    for i in dists:
        print(i)
    print()


# 获取显卡信息
def get_gpu_info():
    print("=" * 40 + "显卡信息" + "=" * 40)
    unit = 1024 * 1024

    pynvml.nvmlInit()  # 初始化
    gpu_derive_info = pynvml.nvmlSystemGetDriverVersion()
    print("Drive版本: ", str(gpu_derive_info))  # 显示驱动信息

    gpu_device_count = pynvml.nvmlDeviceGetCount()  # 获取Nvidia GPU块数
    print("GPU个数：", gpu_device_count)

    for i in range(gpu_device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)  # 获取GPU i的handle，后续通过handle来处理
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)  # 通过handle获取GPU i的信息
        gpu_name = str(pynvml.nvmlDeviceGetName(handle))
        gpu_temperature = pynvml.nvmlDeviceGetTemperature(handle, 0)
        gpu_fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
        gpu_power_state = pynvml.nvmlDeviceGetPowerState(handle)
        gpu_util_rate = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        gpu_memory_rate = pynvml.nvmlDeviceGetUtilizationRates(handle).memory

        print("第 %d 张卡：" % i, "-" * 30)
        print("显卡名：", gpu_name)
        print("内存总容量：", memory_info.total / unit, "MB")
        print("使用容量：", memory_info.used / unit, "MB")
        print("剩余容量：", memory_info.free / unit, "MB")
        print("显存空闲率：", (memory_info.free / memory_info.total) * 100, "%")
        print("温度：", gpu_temperature, "摄氏度")
        # 每分钟转的圈数
        print("风扇速率：", gpu_fan_speed)
        # 几pin供电
        print("供电水平：", gpu_power_state)
        print("gpu计算核心满速使用率：", gpu_util_rate, "%")
        print("gpu内存读写满速使用率：", gpu_memory_rate, "%")
        print("内存占用率：", (memory_info.used / memory_info.total) * 100, "%")
    pynvml.nvmlShutdown()  # 最后关闭管理工具
    print()


# 打印所有的信息
def get_all_info():
    get_system_info()
    get_cpu_info()
    get_memory_info()
    get_disk_info()
    get_python_info()
    get_pip_info()
    get_gpu_info()


if __name__ == '__main__':
    get_all_info()
