# bilibiliPyCrawler

​		使用python构架网络爬虫，实现了广度优先遍历算法、简单随机游走遍历算法、随机游走遍历算法共三种遍历方式，从指定的节点爬取指定数量的用户数据，存入文件中再对其进行处理。生成用户节点之间的无向图进行数据可视化处理，再将待处理的数据存入MySQL中。

###### 	软件架构

运行环境：MySQL Server 8.0、PyCharm Community Edition 2021.3.2  Python3.9

模块： pandas	numpy	pymysql	 time requests networkx matplotlib csv json random jsonpath re 

###### 	数据模型

本项目针对B站用户的UID、用户名、及其被关注用户的UID和用户名进行采集数据。友邻关系定义为该用户的粉丝数、关注数和关注的用户与粉丝。

###### 	字段的物理意义：

- name 		   用户名称
- uname		  关注用户的用户名
- uid			    关注用户的UID
- sex 	          用户的性别
- level		     用户的B站等级
- birthday	    用户的生日	
- coins		    用户的硬币数	

在graph.txt中，用

UID1 UID2 来表示无向图中节点UID1和节点UID2的边 

![image-20231009091438369](C:\Users\25823\AppData\Roaming\Typora\typora-user-images\image-20231009091438369.png)

![image-20231009091449259](C:\Users\25823\AppData\Roaming\Typora\typora-user-images\image-20231009091449259.png)

![image-20231009091456033](C:\Users\25823\AppData\Roaming\Typora\typora-user-images\image-20231009091456033.png)



​		在三种爬取策略中，使用广度优先遍历算法的程序运行效率明显高于使用简单随机游走遍历算法和随机游走遍历算法的程序运行效率。对于广度优先遍历算法，适用于分析粉丝量较大的用户的关系网络，通过该算法爬取的用户都是以一个用户为中心扩散开来。而对于简单随机游走遍历算法和随机游走遍历算法，则适用于分析没有限定主要范围时的用户关系网络。如何选择正确的算法，很大程度上取决于我们的需求，不同的算法对应不同的需求。