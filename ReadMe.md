# TaxCreeper
## Core
1. 核心程序（客户机）：  
[Generator_Distributed.py](https://github.com/FloatingCat/TaxCreeper/blob/main/Generator_Distributed.py)
2. 分布式支持组件：  
生成爬虫队列到云端：  
[URL_Pusher_Redis.py](https://github.com/FloatingCat/TaxCreeper/blob/main/URL_Pusher_Redis.py)  
爬取数据持久化到本地sqlite：  
[Res_Redis_to_SQL.py](https://github.com/FloatingCat/TaxCreeper/blob/main/Res_Redis_to_SQL.py)  
意外情况检测（爬取队列和检测结果集）：  
[Sync_Queue](https://github.com/FloatingCat/TaxCreeper/blob/main/Sync_Queue.py)
## Structure
![Structure](https://raw.githubusercontent.com/FloatingCat/TaxCreeper/main/Doc/Structure_2.jpg)
## TODO:
- 进一步封装
- web端查询开发
    - 检索优化
- 断点续传batch减小

