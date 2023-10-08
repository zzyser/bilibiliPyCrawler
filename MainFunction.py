from GraphSamplingAlgorithms import BFS_sampling
from GraphSamplingAlgorithms import FF_sampling
from GraphSamplingAlgorithms import SRW_sampling
import numpy as np

# 设置随机数的初始种子
np.random.seed(0)

if __name__ == '__main__':
    # 采样节点数
    sampling_node_number = 100000
    # 起始用户id
    start_id = 47655022
    # 采样
    BFS_sampling(sampling_node_number, start_id)
    # SRW_sampling(sampling_node_number, start_id)
    # FF_sampling(sampling_node_number, start_id)
