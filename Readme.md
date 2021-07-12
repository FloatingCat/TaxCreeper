# TaxCreeper V3
## 数据流图
![df](Doc/crawler_dataflow_p0.png)

## 任务队列data bus 
- 目前进度：基于Kafka和FastAPI全面重构，进行中，20%
- 明确一点：同一时间，只应该有一个url存在于流程中，即一个url同一时间只应该有一个状态，故作为主键
- TODO  
    - 日志系统
    - 任务结果
    - 异常任务检测
    
## 爬虫端重构
- TODO
    - 主库同步
    - 协程优化，v2已完成