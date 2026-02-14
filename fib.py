#! /usr/bin/python

import time
import sys
import ctypes
import statistics
import psutil
import math

_libInC = ctypes.CDLL('./libMyLib.so')

def recur_fibo(n):
   if n <= 1:
       return n
   else:
       return(recur_fibo(n-1) + recur_fibo(n-2))

cpu_before = 0
cpu_after = 0


results_pmu_time = []
results_pmu_std = []
results_avg_time = []
results_std_time = []
         
for nterms in range (1,31):
    list_cpu_count = []
    list_cpu_time = []
    cpu_usage = psutil.cpu_percent(interval=0, percpu=True)
    for x in range(3):
            _libInC.init_counters_wrap.argtypes = [ctypes.c_int32, ctypes.c_int32]
            _libInC.init_counters_wrap(1,0)
            cpu_before_py = time.time()
            _libInC.get_cyclecount_wrap.restype = ctypes.c_uint
            cpu_before = _libInC.get_cyclecount_wrap()
            recur_fibo(nterms)
            cpu_after = _libInC.get_cyclecount_wrap()
            cpu_after_py = time.time()
            cpu_count = cpu_after - cpu_before
            cpu_time = cpu_after_py - cpu_before_py
            list_cpu_count.append(cpu_count)
            list_cpu_time.append(cpu_time)
            cpu_usage = psutil.cpu_percent(percpu=True)
            print('CPU usage: {} Trial: {}:'.format (cpu_usage, x))
    print('Term: {}'.format(nterms))
    print(list_cpu_count)
    avg = sum(list_cpu_count)/3
    print('Average CPU Cycle Count: {}'.format(avg))
    std_dev = statistics.stdev(list_cpu_count)
    std_dev = std_dev/(math.sqrt(3))
    print('Standard Deviation CPU Cycle Count: {}'.format(std_dev))
    print(list_cpu_time)
    avg_time = sum(list_cpu_time)/3
    print('Average CPU Time: {}:'.format(avg_time))
    std_dev_time = statistics.stdev(list_cpu_time)
    std_dev_time = std_dev_time/(math.sqrt(3))
    print('Standard Deviation CPU Time: {}'.format(std_dev_time))
    cpu_count_time = avg/650000000
    print('PMU timing based on 650 MHz freqency: {}'.format(cpu_count_time))
    
    
    results_pmu_time.append(cpu_count_time)
    results_pmu_std.append(std_dev/650000000)
    results_avg_time.append(avg_time)
    results_std_time.append(std_dev_time)
        
print('PMU Time: {}'.format(results_pmu_time))
print('Standard Deviation for PMU time: {}'.format(results_pmu_std))
print('Python Time: {}'.format(results_avg_time))
print('Standard Deviation for Python time {}'.format(results_std_time))


        
# check if the number of terms is valid
if nterms <= 0:
   print("Please enter a positive integer")