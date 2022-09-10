import numpy as np
from constants import *

# naive power consumption at a local CPU
def get_local_power_cost(used_cpu, used_tx=0):
    # 返回商和余数的元组
    "1个CPU 有 4GH clock rate"
    cores, remained = divmod(used_cpu, 4*GHZ)
    return cores*(4*GHZ)**3+(remained)**3

def get_fail_cost(failed_to_offload, failed_to_generate):
     # True ： 1
     # False： 0
     return float((failed_to_offload+failed_to_generate)>0) # 返回所有失败的个数

def get_drift_cost(before, after, empty_reward=True):
    before = np.array(before)
    after = np.array(after)
    if sum(after)>sum(before):
        drift = after
    elif empty_reward:
        drift = after-before-(after==0)*before   #?????
    else:
        drift = after-before
    return drift

def total_cost(used_edge_cpus, used_cloud_cpus, drift_cost, option=1): # drift_cost队列长度的变化 option=self.cost_type
    local_cost = 0
    server_cost = 0
    for used_edge_cpu in used_edge_cpus.values():
        "边缘计算"
        local_cost += get_local_power_cost(used_edge_cpu)
    # for used_cloud_cpu in used_cloud_cpus.values():
    #     "云计算"
    #     server_cost += get_local_power_cost(used_cloud_cpu) # == 0  不考虑云端cpu的功耗

    "付费"
    if option==1:
        return aggregate_cost1(local_cost, server_cost, drift_cost)
    elif option==2:
        return aggregate_cost2(local_cost, server_cost, drift_cost)
    else:
        return aggregate_cost0(local_cost, server_cost, drift_cost)

# show graph 5th option
def aggregate_cost0(local_cost, server_cost, quad_drift, gamma_1=0.5, gamma_2=0.0, gamma_3=0.5, V=1e-10/GHZ/GHZ, W=1):
    local_cost /= 900000*64*GHZ**3 #dollars/sec
    server_cost /= 900000*64*GHZ**3 #dollars/sec    == 0
    compute_cost = (local_cost + server_cost)
    # drift cost와 dollar cost가 똑같이 1초에 1달러의 가치를 지닌다고 가정하는 것. 假设漂移成本和美元成本每秒等价 1 美元

    drift_cost = W*sum(quad_drift)

    return compute_cost+drift_cost

def aggregate_cost1(local_cost, server_cost, quad_drift, gamma_1=0.5, gamma_2=0.0, gamma_3=0.5, V=1e-10/GHZ/GHZ, W=1):
    local_cost /= 900000*64*GHZ**3 #dollars/sec
    server_cost /= 900000*64*GHZ**3 #dollars/sec
    compute_cost = (3*local_cost + 1*server_cost)
    # drift cost와 dollar cost가 똑같이 1초에 1달러의 가치를 지닌다고 가정하는 것.

    drift_cost = 2*sum(quad_drift)

    return compute_cost+drift_cost

def aggregate_cost2(local_cost, server_cost, quad_drift, gamma_1=0.5, gamma_2=0.0, gamma_3=0.5, V=1e-10/GHZ/GHZ, W=1):
    local_cost /= 900000*64*GHZ**3 #dollars/sec
    server_cost /= 900000*64*GHZ**3 #dollars/sec
    compute_cost = (1*local_cost + 3*server_cost)
    # drift cost와 dollar cost가 똑같이 1초에 1달러의 가치를 지닌다고 가정하는 것.

    drift_cost = 2*sum(quad_drift)

    return compute_cost+drift_cost
