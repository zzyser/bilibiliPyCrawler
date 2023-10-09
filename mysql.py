import time

import pymysql
import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36 '
}


# 爬取 follower, following
def get_star(url):
    html = requests.get(url, headers=headers).json()['data']
    follower = html['follower']
    following = html['following']
    print("粉丝数：{}，关注数：{}".format(follower, following))
    print("-" * 20)
    time.sleep(0.1)
    return follower, following


# 爬取  name, sex, level, birthday, coins
def get_userdata(url):
    jsondata = requests.get(url, headers=headers).json()['data']
    name = jsondata['name']
    sex = jsondata['sex']
    level = jsondata['level']
    birthday = jsondata['birthday']
    coins = jsondata['coins']
    # print("名字是：{}  性别是：{}  等级是：{}  生日是：{}  硬币数目：{}".format(name, sex, level, birthday, coins))
    time.sleep(0.1)
    return name, sex, level, birthday, coins


# 因为 关注数、粉丝数 和其他数据所用的url不一样，所以在此函数中整合返回值
def getinfo(uid):
    url = "https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp".format(uid)
    name, sex, level, birthday, coins = get_userdata(url)
    url2 = "https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp".format(uid)
    follower, following = get_star(url2)
    return name, sex, level, birthday, coins, follower, following


if __name__ == '__main__':
    # Mysql
    connect = pymysql.Connect(
        # host='192.168.56.20',
        host='localhost',
        user='root',
        passwd='123456',  # 密码根据安装时的来写
        db='b',
        port=3306,
        charset='utf8'
    )
    cursor = connect.cursor()
    cursor.execute("""create database if not exists b;""")  # 重置b数据库
    cursor.execute("""use b;""")  # 使用b数据库
    cursor.execute("""drop table if exists user;""")  # 重置user表
    # 创建user表
    query = """create table user(
        uid int,
        user_name char(40),
        sex char(10),
        user_level int,
        user_birthday char(30),
        user_coins int,
        user_fans int,
        user_following int
    );"""
    cursor.execute(query)
    # 插入数据语句模板，-> cursor.execute(sql % data) 需要插入的数据放入data中
    sql = """insert into user(uid,user_name,sex,user_level,user_birthday,user_coins,user_fans,user_following)
     values ('%d','%s','%s','%d','%s','%d','%d','%d');"""
    # 读取之前  pandas_drop_duplicates文件  创建的id字典，根据这些uid来爬取信息
    with open(r'C:\Game\id_dict.txt', 'r', encoding='utf-8-sig') as fp:
        ids = fp.readlines()
        for i in ids:
            # 例： h = '0 70070',0是顺序，70070是uid，h是个列表， h[1]则是我们需要的 uid
            h = i.split()
            # print(h[1])  h[1] 是uid
            name, sex, level, birthday, coins, follower, following = getinfo(h[1])
            # print(h[1]+type(h[1]))
            # print(name)
            # print(sex)
            # print(level)
            # print(birthday)
            # print(coins)
            # print(follower)
            # print(following)
            data = (int(h[1]), name, sex, level, birthday, coins, follower, following)
            #  ('%d', '%s', '%s', '%d', '%s', '%d', '%d', '%d')
            cursor.execute(sql % data)
            connect.commit()  # 提交查询语句，改变数据库中的数据
            print("插入成功")

