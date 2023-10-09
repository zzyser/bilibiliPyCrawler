import pandas as pd
import numpy as np
import json

# 清洗id生成
data = pd.read_csv(r'C:/Game/graph_data.csv')
print('\n', data.info())
print('\n', data.head())
# 用户id数据
user_id_data = data[['id1', 'id2']]
print('\n', user_id_data.head())
# 用户id唯一值列表
user_id_list = list(set(user_id_data.id1.tolist()) | set(user_id_data.id2.tolist()))
user_id_list.sort()
# 新旧id转换字典
new_id_list = list(range(len(user_id_list)))
dict_id_old_to_new = dict(zip(user_id_list, new_id_list))
dict_id_new_to_old = dict(zip(new_id_list, user_id_list))
# 转换为新id
user_id_data = user_id_data.replace(dict_id_old_to_new)
# 无向图去自环和重边
max_new_id = np.max(new_id_list)
user_id_data['label1'] = user_id_data.apply(lambda x: x.min() * (max_new_id + 1) + x.max(), axis=1)
user_id_data['label2'] = user_id_data.apply(lambda x: x[0] - x[1], axis=1)
user_id_data.drop_duplicates('label1', keep='first', inplace=True)
user_id_data = user_id_data[user_id_data['label2'] != 0]
user_id_data = user_id_data[['id1', 'id2']]
# 存储清洗后的新id数据
with open(r'C:/Game/graph.txt', 'w', encoding='utf-8') as txt:
    for i in range(user_id_data.shape[0]):
        line = json.dumps(eval(str(user_id_data.iloc[i, 0]))) + ' ' + json.dumps(eval(str(user_id_data.iloc[i, 1])))
        txt.write(line + '\n')
txt.close()

# 存储新id转换旧id的字典
with open(r'C:/Game/id_dict.txt', 'w', encoding='utf-8') as txt:
    for key in dict_id_new_to_old.keys():
        line = json.dumps(eval(str(key))) + ' ' + json.dumps(eval(str(dict_id_new_to_old[key])))
        txt.write(line + '\n')
txt.close()


# 读取新id转换旧id的字典
def file2dict(path, delimiter=' '):
    fp = open(path, 'r', encoding='utf-8')
    string = fp.read()
    fp.close()
    row_list = string.splitlines()
    data_dict = {}
    for row in row_list:
        data = row.strip().split(delimiter)
        data_dict[int(data[0])] = int(data[1])
    return data_dict


dict_id_new_to_old = file2dict(r'C:/Game/id_dict.txt')
print('\n', dict_id_new_to_old)
