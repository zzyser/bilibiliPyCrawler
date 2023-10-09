import csv

import numpy as np
from GetNeighbors import GetNeighborList
from random import choice
import pandas as pd


# 广度优先遍历算法
def BFS_sampling(sampling_node_number, start_id):
    node_list = [start_id]
    pointer = 0
    current_node_number = 1
    remain_node_number = sampling_node_number - current_node_number
    # 创建csv文件并定义列索引
    with open(r'C:/Game/graph_data.csv', 'a', newline='', encoding='utf-8-sig') as f:
        csv_write = csv.writer(f, dialect='excel')
        csv_write.writerow(['name1', 'id1', 'name2', 'id2'])
    f.close()
    # 广度优先遍历
    while current_node_number < sampling_node_number:
        cur_id = node_list[pointer]
        user_name, mids_unique, unames_unique = GetNeighborList(cur_id)
        neighbor_number = len(mids_unique)
        new_node_list = []
        for i in range(neighbor_number):
            if remain_node_number > 0:
                # 创建csv文件并定义列索引
                with open(r'C:/Game/graph_data.csv', 'a', newline='', encoding='utf-8-sig') as f:
                    csv_write = csv.writer(f, dialect='excel')
                    csv_write.writerow([user_name, cur_id, unames_unique[i], mids_unique[i]])
                f.close()
                if mids_unique[i] not in node_list:
                    new_node_list.append(mids_unique[i])
                    remain_node_number = remain_node_number - 1
            else:
                break
        node_list.extend(new_node_list)
        current_node_number = current_node_number + len(new_node_list)
        pointer = pointer + 1

    print('已爬取节点数：', len(node_list))


# 随机森林算法
def FF_sampling(sampling_node_number, start_id):
    node_list = []
    node_list.append(start_id)
    pointer = 0
    current_node_number = 1
    remain_node_number = sampling_node_number - current_node_number
    # 创建csv文件并定义列索引
    with open(r'C:/Game/graph_data.csv', 'a', newline='', encoding='utf-8-sig') as f:
        csv_write = csv.writer(f, dialect='excel')
        csv_write.writerow(['name1', 'id1', 'name2', 'id2'])
    f.close()
    # 森林火随机算法
    while current_node_number < sampling_node_number:

        # 当pointer>=len(node_list)时随机生成一个新的种子节点
        if pointer >= len(node_list):
            candidate_seeds = set(range(1, 2 * sampling_node_number)) - set(node_list)
            seed = choice(list(candidate_seeds))
            print('seed:', seed)
            node_list.append(seed)
            current_node_number = current_node_number + 1
            remain_node_number = remain_node_number - 1

        cur_id = node_list[pointer]
        user_name, mids_unique, unames_unique = GetNeighborList(cur_id)
        neighbor_number = len(mids_unique)
        # 生成几何分布的随机数random_k
        random_k = np.random.geometric(0.7)
        new_node_list = []
        new_name_list = []
        for i in range(neighbor_number):
            if mids_unique[i] in node_list:
                # 创建csv文件并定义列索引
                with open(r'C:/Game/graph_data.csv', 'a', newline='', encoding='utf-8-sig') as f:
                    csv_write = csv.writer(f, dialect='excel')
                    csv_write.writerow([user_name, cur_id, unames_unique[i], mids_unique[i]])
                f.close()
            else:
                new_node_list.append(mids_unique[i])
                new_name_list.append(unames_unique[i])
        print('new_node_list:', len(new_node_list))
        k_list = []
        while len(k_list) < random_k and len(new_node_list) > 0 and remain_node_number > 0:
            random_position = np.random.randint(len(new_node_list), size=[1])[0]
            # print(random_position)
            extracted_node = new_node_list[random_position]
            extracted_name = new_name_list[random_position]
            k_list.append(extracted_node)
            new_node_list.remove(extracted_node)
            new_name_list.remove(extracted_name)
            remain_node_number = remain_node_number - 1
            # 创建csv文件并定义列索引
            with open(r'C:/Game/graph_data.csv', 'a', newline='', encoding='utf-8-sig') as f:
                csv_write = csv.writer(f, dialect='excel')
                csv_write.writerow([user_name, cur_id, extracted_name, extracted_node])
            f.close()
        print('k_list:', len(k_list))
        node_list.extend(k_list)
        current_node_number = current_node_number + len(k_list)
        pointer = pointer + 1
        print('已爬取节点数：', len(node_list))


# 简单随机游走算法
def SRW_sampling(sampling_node_number, start_id):
    node_list = []
    current_node_number = 0
    # 创建csv文件并定义列索引
    with open(r'C:/Game/graph_data.csv', 'a', newline='', encoding='utf-8-sig') as f:
        csv_write = csv.writer(f, dialect='excel')
        csv_write.writerow(['name1', 'id1', 'name2', 'id2'])
    f.close()
    # 定义存储相邻节点信息的DataFrame对象
    Neighbors = pd.DataFrame(np.zeros([sampling_node_number, 4]),
                             columns=['id', 'id_name', 'neighbor_ids', 'neighbor_names'])
    pointer = -1
    # 初始化随机旅行者
    walker = start_id
    while current_node_number < sampling_node_number:
        random_value = np.random.random()
        if random_value < 0.15:
            walker = start_id
        if walker not in node_list:
            user_name, mids_unique, unames_unique = GetNeighborList(walker)
            pointer = pointer + 1
            Neighbors.iloc[pointer, 0] = walker
            Neighbors.iloc[pointer, 1] = user_name
            Neighbors.iloc[pointer, 2] = ','.join([str(i) for i in mids_unique])
            Neighbors.iloc[pointer, 3] = ','.join(unames_unique)
            node_list.append(walker)
            current_node_number = current_node_number + 1
        else:
            cur_pointer = node_list.index(walker)
            user_name = Neighbors.iloc[cur_pointer, 1]
            cur_neighbors = Neighbors.iloc[cur_pointer, 2]
            cur_neighbors = cur_neighbors.split(',')
            if cur_neighbors[0] == '':
                mids_unique = []
            else:
                mids_unique = list(map(int, cur_neighbors))
            cur_neighbors = Neighbors.iloc[cur_pointer, 3]
            unames_unique = cur_neighbors.split(',')
        neighbor_number = len(mids_unique)
        if neighbor_number > 0:
            start_walker = walker
            random_position = np.random.randint(len(mids_unique))
            walker = mids_unique[random_position]
            walker_name = unames_unique[random_position]
            # 创建csv文件并存储关注边
            with open(r'C:/Game/graph_data.csv', 'a', newline='', encoding='utf-8-sig') as f:
                csv_write = csv.writer(f, dialect='excel')
                csv_write.writerow([user_name, start_walker, walker_name, walker])
            f.close()
        else:
            walker = start_id
        print(current_node_number)
