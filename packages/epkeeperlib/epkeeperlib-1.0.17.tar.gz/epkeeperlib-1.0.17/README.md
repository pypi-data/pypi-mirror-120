# epkeeperlib通用包

## common
通用模块
***
> - utils  
> 通用工具  
> `divide` 除法函数。可指定小数点位数，可生成占比、增减比例的百分值  
> `print_df` 打印pd.DataFrame。可直接复制进excel  
> `create_path` 若不存在该路径，则创建该路径  

## bill
电费账单相关工具
***
> - ep_calc  
> 电能计算工具  
> `get_ele_use` 根据输入的电能值的时间序列（pd.Series），输出用电量  


> - monitor_bill  
> 监控电费账单计算工具  
> `get_unit_price` 根据输入的电价参数匹配到相应的电价信息（pd.DataFrame）  
> `get_pf_adjust_rate` 功率因数调整比例计算函数  


> - tou  
> 分时段工具  
> `TOU_HOUR` 每个省份的分时段参数  
> `get_season_code` 获取电价的季节码（夏季、非夏季）  
> `get_tou_hour` 获取分时段小时  

## db
数据库工具
***
> - mysql_pool  
> MySQL工具  
> `MysqlPool` MySQL连接类  
> `mysql_fetch_data` MySQL数据获取函数   
> `mysql_execute` MySQL执行函数  
> `mysql_insert_df` 插入pd.DataFrame至MySQL数据库  


> - fetch_monitor  
> 监控数据获取工具  
> `get_oa_monitor_data` 获取OA监控数据库函数  


> - sql_faraday  
> 法拉第数据库SQL语句  
> `FARADAY_BILL_SQL` 账单SQL  
> `FARADAY_TARIFF_SQL` 电价表SQL  
> `FARADAY_TIME_OF_USE_SQL` 分时段表SQL  
> `FARADAY_INSPECT_RECORD_SQL` 巡检记录SQL  
> `FARADAY_DEFECT_RECORD_SQL` 缺陷记录SQL  


> - sql_oa  
> OA数据库SQL语句  
> `OA_USER_INFO_SQL` 用户基本信息SQL  
> `OA_USER_ELECTRICITY_SQL` 用户电气信息SQL  
> `OA_INSPECT_RECORD_SQL` 巡检记录SQL  
> `OA_MONITOR_INFO_SQL` 监控信息SQL  
> `OA_MONITOR_ALERT_SQL` 监控告警记录SQL  
> `OA_MAINTENANCE_SQL` 工程维护信息SQL  
> `OA_DEFECT_RECORD_SQL` 缺陷记录SQL  

## nrel
REopt_Lite_API接口 
***
> - post_and_poll  
> `get_api_results` Function for posting job and polling results end-point  
> `get_run_uuid` Function for posting job   

> - results_poller  
> `poller` Function for polling the REopt API results URL until status is not "Optimizing..." 
